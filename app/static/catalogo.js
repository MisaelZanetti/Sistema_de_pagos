(() => {
    // Los productos vienen del backend: app/modules/vista_productos/services.py
    // los serializa a JSON y el template los embebe en #catalogo-productos.
    const productos = (() => {
        const nodo = document.getElementById('catalogo-productos');
        if (!nodo) return [];
        try {
            return JSON.parse(nodo.textContent);
        } catch (e) {
            console.error('No se pudo leer el catálogo', e);
            return [];
        }
    })();
    const products = productos;
    const $ = id => document.getElementById(id);
    const money = n => '$ ' + new Intl.NumberFormat('es-AR', { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(n);
    const normalize = s => (s || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
    const precioMax = products.reduce((m, p) => Math.max(m, p.price), 0);
    const state = { query: '', maxPrice: precioMax, stockOnly: false, sort: 'featured' };
    const icon = name => ({ chip: '<rect x="6" y="6" width="12" height="12" rx="2"/><rect x="9" y="9" width="6" height="6" rx="1"/><path d="M9 2v4m6-4v4M9 18v4m6-4v4M2 9h4m-4 6h4m12-6h4m-4 6h4"/>', gpu: '<rect x="3" y="6" width="18" height="12" rx="2"/><circle cx="9" cy="12" r="3"/><circle cx="16" cy="12" r="3"/>', board: '<rect x="4" y="2" width="16" height="20" rx="2"/><rect x="7" y="6" width="6" height="6" rx="1"/><path d="M16 6v8M7 16h10"/>', memory: '<rect x="2" y="7" width="20" height="10" rx="1.5"/><path d="M6 10h3v4H6zm9 0h3v4h-3zM6 17v3m4-3v3m4-3v3m4-3v3"/>', storage: '<rect x="4" y="3" width="16" height="18" rx="2"/><circle cx="12" cy="10" r="4"/><path d="m12 10 4 4M8 18h8"/>', power: '<rect x="3" y="5" width="18" height="15" rx="2"/><path d="m13 8-4 5h5l-3 4"/>', case: '<rect x="6" y="2" width="12" height="20" rx="2"/><circle cx="12" cy="9" r="3"/><circle cx="12" cy="16" r="3"/>', cooling: '<rect x="3" y="3" width="18" height="18" rx="3"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="1.5"/>' })[name] || '<rect x="4" y="4" width="16" height="16" rx="2"/>';
    const svg = (name, size = 22) => `<svg width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${icon(name)}</svg>`;
    function fan() { return '<div class="fan"><div class="fan-blades"></div><span class="fan-hub"></span></div>' }
    function visual(type) {
        if (type === 'gpu') return `<div class="gpu-object"><div class="gpu-top">GEFORCE RTX <span>MSI</span></div><div class="gpu-body">${fan()}<div class="gpu-center">MSI</div>${fan()}</div><div class="gpu-connector"></div></div>`;
        if (type === 'cpu' || type === 'intel') return `<div class="cpu-box ${type}"><div class="cpu-box-top"></div><div class="cpu-box-face"><small>${type === 'intel' ? 'intel' : 'AMD'}</small><span>${type === 'intel' ? 'CORE' : 'RYZEN'}</span><b>${type === 'intel' ? 'i5' : '7'}</b><em>${type === 'intel' ? 'UNLOCKED' : '9000 SERIES'}</em></div><div class="cpu-box-side"></div></div>`;
        if (type === 'ram') return '<div class="ram-object"><div class="ram-stick stick-0"><div class="ram-light"></div><div class="ram-heatsink"><small>CORSAIR</small><b>VENGEANCE</b><span>DDR5</span></div><div class="ram-pins"></div></div><div class="ram-stick stick-1"><div class="ram-light"></div><div class="ram-heatsink"><small>CORSAIR</small><b>VENGEANCE</b><span>DDR5</span></div><div class="ram-pins"></div></div></div>';
        if (type === 'board') return '<div class="motherboard"><div class="board-io">TUF<br>GAMING</div><div class="board-socket"><span></span></div><div class="board-ram"><i></i><i></i><i></i><i></i></div><div class="board-sink">TUF GAMING</div><div class="board-slots"><i></i><i></i><i></i></div><div class="board-chip"></div><div class="board-battery"></div></div>';
        if (type === 'ssd') return '<div class="ssd-object"><div class="ssd-label"><b>SAMSUNG</b><strong>990 <span>PRO</span></strong><small>PCIe 4.0 NVMe M.2 SSD</small><em>1TB</em></div><div class="ssd-pins"></div></div>';
        if (type === 'power') return `<div class="psu-object"><div class="psu-top">${fan()}</div><div class="psu-front"><small>CORSAIR</small><strong>RM<span>750</span>e</strong><i>80 PLUS GOLD</i></div><div class="psu-side"><i></i><i></i><i></i><i></i></div></div>`;
        if (type === 'case') return `<div class="case-object"><div class="case-side"><div class="case-inside">${fan()}<div class="case-card"></div><div class="case-psu">NZXT</div></div></div><div class="case-front">${fan()}${fan()}<small>NZXT</small></div><div class="case-top"></div></div>`;
        return `<div class="cooler-object"><div class="cooler-fins"></div><div class="cooler-face">${fan()}</div><div class="cooler-pipes"><i></i><i></i><i></i></div></div>`;
    }
    function filteredProducts() {
        return products
            .filter(p => p.price <= state.maxPrice
                && (!state.stockOnly || p.stock)
                && normalize(`${p.name} ${p.detail}`).includes(normalize(state.query)))
            .sort((a, b) => state.sort === 'price-asc' ? a.price - b.price
                : state.sort === 'price-desc' ? b.price - a.price
                : state.sort === 'name' ? a.name.localeCompare(b.name)
                : b.stock_count - a.stock_count || a.id - b.id);
    }

    function card(p) {
        const stock = p.stock
            ? `<p class="stock"><span></span>Disponible${p.stock_count > 1 ? ` (${p.stock_count})` : ''}</p>`
            : `<p class="stock unavailable"><span></span>Sin stock por el momento</p>`;
        return `<article class="product-card">
            <div class="product-image">
                <div class="product-visual"><span>Sin imagen</span></div>
            </div>
            <div class="product-info">
                <h3>${escapeHtml(p.name)}</h3>
                ${p.detail ? `<p class="product-description">${escapeHtml(p.detail)}</p>` : ''}
                ${stock}
                <div class="product-price"><strong>${money(p.price)}</strong></div>
            </div>
        </article>`;
    }

    // Los nombres y descripciones vienen de la base, así que se escapan
    // antes de inyectarlos con innerHTML.
    function escapeHtml(s) {
        return String(s).replace(/[&<>"']/g, c => (
            { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]
        ));
    }

    function filterCount() {
        return (state.maxPrice < precioMax ? 1 : 0) + (state.stockOnly ? 1 : 0);
    }

    function render() {
        const all = filteredProducts();

        $('product-grid').innerHTML = all.map(card).join('');
        $('catalog-results-count').textContent = all.length;
        $('total-count').textContent = all.length;
        $('empty-state').hidden = all.length > 0;
        $('product-grid').hidden = all.length === 0;
        $('filter-counter').hidden = filterCount() === 0;
        $('filter-counter').textContent = filterCount();

        const activos = [];
        if (state.maxPrice < precioMax) activos.push('Hasta ' + money(state.maxPrice));
        if (state.stockOnly) activos.push('Solo disponibles');
        if (state.query) activos.push(`"${state.query}"`);
        $('active-filters').innerHTML = activos
            .map(v => `<button data-remove-filter="${escapeHtml(v)}">${escapeHtml(v)} ×</button>`)
            .join('');
    }

    function reset() {
        Object.assign(state, { query: '', maxPrice: precioMax, stockOnly: false, sort: 'featured' });
        $('search-input').value = '';
        $('price-range').value = String(precioMax);
        $('price-value').textContent = money(precioMax);
        $('stock-only').checked = false;
        $('sort-select').value = 'featured';
        render();
    }

    $('year').textContent = new Date().getFullYear();
    $('price-range').max = String(precioMax);
    $('price-range').value = String(precioMax);
    $('price-value').textContent = money(precioMax);
    $('hero-gpu').innerHTML = '<div class="product-visual"><span>TecnoPC</span></div>';

    $('price-range').addEventListener('input', e => {
        state.maxPrice = Number(e.target.value);
        $('price-value').textContent = money(state.maxPrice);
        render();
    });

    $('stock-only').addEventListener('change', e => {
        state.stockOnly = e.target.checked;
        render();
    });

    $('search-input').addEventListener('input', e => {
        state.query = e.target.value;
        render();
    });

    $('sort-select').addEventListener('change', e => {
        state.sort = e.target.value;
        render();
    });

    $('reset-filters').addEventListener('click', reset);

    $('active-filters').addEventListener('click', e => {
        const btn = e.target.closest('button[data-remove-filter]');
        if (!btn) return;
        const valor = btn.dataset.removeFilter;
        if (valor === 'Solo disponibles') state.stockOnly = false;
        else if (valor.startsWith('Hasta ')) state.maxPrice = precioMax;
        else { state.query = ''; $('search-input').value = ''; }
        $('price-range').value = String(state.maxPrice);
        $('price-value').textContent = money(state.maxPrice);
        $('stock-only').checked = state.stockOnly;
        render();
    });

    render();
})();
