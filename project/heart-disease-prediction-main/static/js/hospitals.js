(() => {
    const form = document.getElementById('hospital-search');
    if (!form) return;
    const button = document.getElementById('hospital-button');
    const status = document.getElementById('hospital-status');
    const results = document.getElementById('hospital-results');
    const list = document.getElementById('hospital-list');
    const textElement = (tag, text, className) => {
        const node = document.createElement(tag);
        node.textContent = text;
        if (className) node.className = className;
        return node;
    };
    const externalLink = (text, href) => {
        const link = textElement('a', text);
        link.href = href;
        link.target = '_blank';
        link.rel = 'noopener noreferrer';
        return link;
    };
    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        if (button.disabled) return;
        results.hidden = true;
        list.replaceChildren();
        if (!window.isSecureContext || !navigator.geolocation) {
            status.textContent = 'Location is unavailable in this browser. Use the Google Maps link below, or open this page on localhost or HTTPS.';
            return;
        }
        button.disabled = true;
        form.setAttribute('aria-busy', 'true');
        status.textContent = 'Waiting for your location permission…';
        try {
            const position = await new Promise((resolve, reject) => {
                navigator.geolocation.getCurrentPosition(resolve, reject, {
                    timeout: 12000, maximumAge: 60000, enableHighAccuracy: false,
                });
            });
            status.textContent = 'Finding nearby hospitals…';
            const controller = new AbortController();
            const timeout = setTimeout(() => controller.abort(), 15000);
            let response, data;
            try {
                response = await fetch(form.action, {
                    method: 'POST', credentials: 'same-origin',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value,
                    },
                    body: JSON.stringify({latitude: position.coords.latitude,
                        longitude: position.coords.longitude,
                        radius: Number(document.getElementById('hospital-radius').value)}),
                    signal: controller.signal,
                });
                if (response.status === 403) throw new Error('Your session has expired. Refresh the page and try again.');
                if (!(response.headers.get('content-type') || '').includes('application/json')) {
                    throw new Error('Hospital search is unavailable. Refresh the page and try again.');
                }
                data = await response.json();
            } finally {
                clearTimeout(timeout);
            }
            if (!response.ok) throw new Error(data.error || 'Hospital search is unavailable.');
            for (const hospital of data.hospitals) {
                const card = textElement('article', '', 'hospital-card');
                card.append(textElement('h3', hospital.name), textElement('p', hospital.address));
                if (typeof hospital.rating === 'number') {
                    card.append(textElement('p', `${hospital.rating.toFixed(1)} / 5 · ${hospital.rating_count} Google ratings`, 'hospital-rating'));
                }
                if (hospital.maps_url) card.append(externalLink('View on Google Maps', hospital.maps_url));
                for (const source of hospital.attributions) {
                    const attribution = textElement('p', '', 'hospital-note');
                    attribution.append(source.url ? externalLink(source.name, source.url) : textElement('span', source.name));
                    card.append(attribution);
                }
                list.append(card);
            }
            results.hidden = false;
            status.textContent = data.hospitals.length
                ? `Found ${data.hospitals.length} hospitals. Results are ranked by distance.`
                : 'No hospitals found within this radius. Try a wider search area.';
        } catch (error) {
            const locationErrors = {
                1: 'Location permission was denied. Allow location in your browser settings or use Google Maps below.',
                2: 'Your location could not be determined. Please try again or use Google Maps below.',
                3: 'Getting your location took too long. Please try again or use Google Maps below.',
            };
            status.textContent = locationErrors[error.code] || (error.name === 'AbortError'
                ? 'The search timed out. Please try again.'
                : error.message || 'Unable to search. Check your connection and try again.');
        } finally {
            button.disabled = false;
            form.removeAttribute('aria-busy');
        }
    });
})();
