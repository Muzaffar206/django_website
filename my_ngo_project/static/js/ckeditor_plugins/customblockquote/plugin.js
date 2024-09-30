ClassicEditor.builtinPlugins.push(class CustomBlockQuotePlugin {
    init() {
        const editor = this.editor;

        editor.conversion.for('upcast').elementToElement({
            view: {
                name: 'div',
                classes: 'quote-with-text'
            },
            model: 'customBlockQuote'
        });

        editor.conversion.for('dataDowncast').elementToElement({
            model: 'customBlockQuote',
            view: (modelElement, {writer: viewWriter}) => {
                const div = viewWriter.createContainerElement('div', {class: 'quote-with-text'});
                const quoteDiv = viewWriter.createContainerElement('div', {class: 'quote'});
                const svg = viewWriter.createRawElement('svg', {
                    xmlns: 'http://www.w3.org/2000/svg',
                    width: '76',
                    height: '54',
                    viewBox: '0 0 76 54',
                    fill: 'none'
                }, function(domElement) {
                    domElement.innerHTML = '<path d="M67.1429 32.4V30.4H65.1429H54.2857C49.3919 30.4 45.4286 26.4424 45.4286 21.6V10.8C45.4286 5.95763 49.3919 2 54.2857 2H65.1429C70.0366 2 74 5.95763 74 10.8V16.2V21.6V33.75C74 43.8236 65.7956 52 55.6429 52H54.2857C52.3776 52 50.8571 50.4724 50.8571 48.6C50.8571 46.7276 52.3776 45.2 54.2857 45.2H55.6429C61.9794 45.2 67.1429 40.0789 67.1429 33.75V32.4ZM23.7143 32.4V30.4H21.7143H10.8571C5.96336 30.4 2 26.4424 2 21.6V10.8C2 5.95763 5.96336 2 10.8571 2H21.7143C26.6081 2 30.5714 5.95763 30.5714 10.8V16.2V21.6V33.75C30.5714 43.8236 22.367 52 12.2143 52H10.8571C8.94907 52 7.42857 50.4724 7.42857 48.6C7.42857 46.7276 8.94907 45.2 10.8571 45.2H12.2143C18.5509 45.2 23.7143 40.0789 23.7143 33.75V32.4Z" stroke="#090E0D" stroke-width="4"/>';
                });
                viewWriter.insert(viewWriter.createPositionAt(quoteDiv, 0), svg);
                viewWriter.insert(viewWriter.createPositionAt(div, 0), quoteDiv);
                return div;
            }
        });

        editor.conversion.for('editingDowncast').elementToElement({
            model: 'customBlockQuote',
            view: (modelElement, {writer: viewWriter}) => {
                const div = viewWriter.createContainerElement('div', {class: 'quote-with-text'});
                const quoteDiv = viewWriter.createContainerElement('div', {class: 'quote'});
                const svg = viewWriter.createRawElement('svg', {
                    xmlns: 'http://www.w3.org/2000/svg',
                    width: '76',
                    height: '54',
                    viewBox: '0 0 76 54',
                    fill: 'none'
                }, function(domElement) {
                    domElement.innerHTML = '<path d="M67.1429 32.4V30.4H65.1429H54.2857C49.3919 30.4 45.4286 26.4424 45.4286 21.6V10.8C45.4286 5.95763 49.3919 2 54.2857 2H65.1429C70.0366 2 74 5.95763 74 10.8V16.2V21.6V33.75C74 43.8236 65.7956 52 55.6429 52H54.2857C52.3776 52 50.8571 50.4724 50.8571 48.6C50.8571 46.7276 52.3776 45.2 54.2857 45.2H55.6429C61.9794 45.2 67.1429 40.0789 67.1429 33.75V32.4ZM23.7143 32.4V30.4H21.7143H10.8571C5.96336 30.4 2 26.4424 2 21.6V10.8C2 5.95763 5.96336 2 10.8571 2H21.7143C26.6081 2 30.5714 5.95763 30.5714 10.8V16.2V21.6V33.75C30.5714 43.8236 22.367 52 12.2143 52H10.8571C8.94907 52 7.42857 50.4724 7.42857 48.6C7.42857 46.7276 8.94907 45.2 10.8571 45.2H12.2143C18.5509 45.2 23.7143 40.0789 23.7143 33.75V32.4Z" stroke="#090E0D" stroke-width="4"/>';
                });
                viewWriter.insert(viewWriter.createPositionAt(quoteDiv, 0), svg);
                viewWriter.insert(viewWriter.createPositionAt(div, 0), quoteDiv);
                return div;
            }
        });

        editor.model.schema.register('customBlockQuote', {
            inheritAllFrom: '$block'
        });
    }
});