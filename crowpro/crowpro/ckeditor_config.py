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
                'code','codeblock',
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
            'toolbar': ['imageTextAlternative', '|', 'imageStyle:alignLeft',
                        'imageStyle:alignRight', 'imageStyle:alignCenter', 'imageStyle:side', '|'],
            'styles': [
                'full',
                'side',
                'alignLeft',
                'alignRight',
                'alignCenter',
            ]

        },
        'table': {
            'contentToolbar': ['tableColumn', 'tableRow', 'mergeTableCells',
                               'tableProperties', 'tableCellProperties'],
        },
        'heading': {
            'options': [
                    # { model: 'paragraph', title: 'Paragraph'},
                    # { model: 'heading1', view: 'h1', title: 'Heading 1'},
                    # { model: 'heading2', view: 'h2', title: 'Heading 2'},
                    # { model: 'heading3', view: 'h3', title: 'Heading 3'},
                    # { model: 'heading4', view: 'h4', title: 'Heading 4'},
                    # { model: 'heading5', view: 'h5', title: 'Heading 5'},
                    # { model: 'heading6', view: 'h6', title: 'Heading 6'},
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
    "default": {"BACKEND": "blog.storage.CustomStorage"},
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

CKEDITOR_5_FILE_UPLOAD_PERMISSION = "authenticated"
