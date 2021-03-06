function checkboxTreeview() {

    $('input[type="checkbox"]').change(checkboxChanged);

    function checkboxChanged() {
        let $this = $(this),
            checked = $this.prop("checked"),
            container = $this.parent(),
            siblings = container.siblings();

        container.find('input[type="checkbox"]')
            .prop({
                indeterminate: false,
                checked: checked
            })
            .siblings('label')
            .removeClass('custom-checked custom-unchecked custom-indeterminate')
            .addClass(checked ? 'custom-checked' : 'custom-unchecked');

        if (!$this.next().is('ul')) {
            checked
                ? setCookie($this.attr('name'), '', -1)
                : setCookie($this.attr('name'), 'no', 365);
        } else {
            if (checked) {
                for (let chkboxEl of $this.next().find('[type="checkbox"]')) {
                    setCookie(chkboxEl.name, '', -1);
                }
            } else {
                for (let chkboxEl of $this.next().find('[type="checkbox"]')) {
                    setCookie(chkboxEl.name, 'no', 365);
                }
            }
        }

        checkSiblings(container, checked);
    }

    function checkSiblings($el, checked) {
        let parent = $el.parent().parent(),
            all = true,
            indeterminate = false;

        $el.siblings().each(function () {
            return all = ($(this).children('input[type="checkbox"]').prop("checked") === checked);
        });

        if (all && checked) {
            parent.children('input[type="checkbox"]')
                .prop({
                    indeterminate: false,
                    checked: checked
                })
                .siblings('label')
                .removeClass('custom-checked custom-unchecked custom-indeterminate')
                .addClass(checked ? 'custom-checked' : 'custom-unchecked');

            checkSiblings(parent, checked);
        } else if (all && !checked) {
            indeterminate = parent.find('input[type="checkbox"]:checked').length > 0;

            parent.children('input[type="checkbox"]')
                .prop("checked", checked)
                .prop("indeterminate", indeterminate)
                .siblings('label')
                .removeClass('custom-checked custom-unchecked custom-indeterminate')
                .addClass(indeterminate ? 'custom-indeterminate' : (checked ? 'custom-checked' : 'custom-unchecked'));

            checkSiblings(parent, checked);
        } else {
            $el.parents("li").children('input[type="checkbox"]')
                .prop({
                    indeterminate: true,
                    checked: false
                })
                .siblings('label')
                .removeClass('custom-checked custom-unchecked custom-indeterminate')
                .addClass('custom-indeterminate');
        }
    }
};
