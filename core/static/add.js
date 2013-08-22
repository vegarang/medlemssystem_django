Ext.require([
    'Ext.form.*'
]);

Ext.onReady(function() {

    var formPanel = Ext.create('Ext.form.Panel', {
        renderTo: Ext.getBody(),
        frame: true,
        title: 'Add member',
        width: 700,
        height: 200,
        bodyPadding: 5,

        fieldDefaults: {
            labelAlign: 'left',
            labelWidth: 90,
            anchor: '100%'
        },

        items: [{
            xtype: 'textfield',
            name: 'name',
            fieldLabel: 'Name',
        },{
            xtype: 'textfield',
            name: 'email',
            fieldLabel: '(optional) email',
        },{
            xtype: 'checkboxfield',
            name: 'lifetime',
            fieldLabel: 'Lifetime membership',
        },{
            xtype: 'button',
            name: 'savebtn',
            text: 'Save',
            scale: 'large',
            listeners:{
                click: function() {
                    
                }
            }
        }]
    });

    formPanel.render();

});
