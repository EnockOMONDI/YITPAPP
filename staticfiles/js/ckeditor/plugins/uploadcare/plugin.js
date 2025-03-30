CKEDITOR.plugins.add('uploadcare', {
    init: function(editor) {
        editor.addCommand('uploadcare', {
            exec: function(editor) {
                uploadcare.openDialog().done(function(file) {
                    file.done(function(fileInfo) {
                        editor.insertHtml('<img src="' + fileInfo.cdnUrl + '"/>');
                    });
                });
            }
        });
        
        editor.ui.addButton('Uploadcare', {
            label: 'Upload Image',
            command: 'uploadcare',
            toolbar: 'insert'
        });
    }
});