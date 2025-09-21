CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': [
            'undo',
            'redo',
            'findAndReplace',
            '|',
            'bold',
            'italic',
            'strikethrough',
            'superscript',
            'subscript',
            'horizontalLine',
            'specialCharacters',
            'code',
            'codeblock',
            '|',
            'sourceEditing',
            'htmlEmbed',
            'pageBreak',
            'showBlocks',
            '|',
            'alignment',
            'fontFamily',
            'fontSize',
            'fontColor',
            'fontBackgroundColor',
            '|',
            'bulletedList',
            'numberedList',
            'todoList',
            'outdent',
            'indent',
            'link',
            '|',
            'uploadImage',
            'fileUpload',
            'insertTable',
            'blockQuote',
            'mediaEmbed',
            '|',
            'heading',
            '|',
        ],

    },
    'extends': {
        'blockToolbar': [
            'paragraph', 'heading1', 'heading2', 'heading3',
            '|',
            'bulletedList', 'numberedList',
            '|',
            'blockQuote',
        ],
        'toolbar': {
            'items': [
                'undo', 'redo', 'findAndReplace',
                '|',
                'heading',
                '|',
                'bold', 'italic', 'strikethrough', 'superscript', 'subscript', 'horizontalLine', 'specialCharacters',
                '|'
                'code', 'codeblock',
                '|',
                'sourceEditing', 'htmlEmbed', 'pageBreak', 'showBlocks',
                '|',
                'alignment', 'fontFamily', 'fontSize', 'fontColor', 'fontBackgroundColor',
                '|',
                'bulletedList', 'numberedList', 'todoList', 'outdent', 'indent', 'link',
                '|',
                'uploadImage', 'insertTable', 'blockQuote', 'mediaEmbed',
            ],
            'shouldNotGroupWhenFull': 'true'
        },
        'image': {
            'toolbar': [
                'imageTextAlternative', 'toggleImageCaption', '|', 'imageStyle:inline', 'imageStyle:wrapText',
                'imageStyle:breakText', '|', 'resizeImage', 'imageStyle:alignRight', 'imageStyle:alignCenter',
                'imageStyle:side',
            ],
            'styles': [
                'full',
                'side',
                'alignLeft',
                'alignRight',
                'alignCenter',
            ],
            'resizeOptions': [
                {'name': 'resizeImage:original', 'label': 'Default image width', 'value': None},
                {'name': 'resizeImage:50', 'label': '50% page width', 'value': '50'},
                {'name': 'resizeImage:75', 'label': '75% page width', 'value': '75'},
                {'name': 'resizeImage:25', 'label': '25% page width', 'value': '25'},
                {'name': 'resizeImage:60', 'label': '60% page width', 'value': '60'},
                {'name': 'resizeImage:40', 'label': '40% page width', 'value': '40'},
            ],
        },
        'table': {
            'contentToolbar': ['tableColumn', 'tableRow', 'toggleTableCaption', 'mergeTableCells',
                               'tableProperties', 'tableCellProperties'],
        },
        'heading': {
            'options': [
                {'model': 'paragraph', 'title': 'Paragraph', 'class': 'ck-heading_paragraph'},
                {'model': 'heading1', 'view': 'h1', 'title': 'Heading 1', 'class': 'ck-heading_heading1'},
                {'model': 'heading2', 'view': 'h2', 'title': 'Heading 2', 'class': 'ck-heading_heading2'},
                {'model': 'heading3', 'view': 'h3', 'title': 'Heading 3', 'class': 'ck-heading_heading3'}
            ]
        }
    },
    'list': {
        'properties': {
            'styles': 'true',
            'startIndex': 'true',
            'reversed': 'true',
        }
    },
    "link": {"defaultProtocol": "https://"},
    "htmlSupport": {
        "allow": [
            {"name": "/.*/", "attributes": True, "classes": True, "styles": True},
        ],
    },
}
STORAGES = {
    "default": {"BACKEND": "storages.backends.dropbox.DropBoxStorage"},
    "staticfiles": {
        "BACKEND": "storages.backends.dropbox.DropBoxStorage",
    },
}

CKEDITOR_5_FILE_UPLOAD_PERMISSION = "authenticated"
