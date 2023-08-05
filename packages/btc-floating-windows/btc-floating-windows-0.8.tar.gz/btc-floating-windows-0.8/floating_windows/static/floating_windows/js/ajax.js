// Floating AJAX: basic functions for loading content.

const floating_ajax = {
    makeRequest: function(options, callback) {
        const container = $(options['container']);

        if (options['preloader']) {
            // upon completion of AJAX, the preloader object executes callback functions.
            options['preloader'].preloaderMessage(container, $.ajax(options), function (response) {
                callback(response, container);
            }, options['icon'], options['text'], options['error_icon'], options['error_text']);
        } else {
            $.when($.ajax(options)).then(function (response) {
                callback(response, container);
            })
        }
    },
    ajaxGetRequest: function(options, callback=null) {
        // the basic function for loading content with an ajax GET request.

        options['type'] = 'GET';
        floating_ajax.makeRequest(options, function (response, container) {
            options['data_type'] === 'JSON' ?
                container.empty().append(response[options['template_var']]) :
                container.empty().append(response);

            // call callback functions.
            if(callback) {
                callback(response, container);
            }
        });

    },

    ajaxPostRequest: function(options, callback=null) {
        // basic function for sending POST requests via ajax.

        options['type'] = 'POST';
        floating_ajax.makeRequest(options, function (response, container) {
            if (callback) {
                callback(response, container);
            }
        });
    },

    gText: function(text, exprForReplace=/_/g, replaceBy=' ') {
        // remove under underscore from text string.
        let result = null;

        if (text) {
            result = text.toString().replace(exprForReplace, replaceBy);
        }

        return result;
    }
};

let floating_full_screen_messenger = undefined;
function Messages(){
    // service for displaying messages to the user about any operations.

    this.fullScreen = function () {
        // message - fill the screen (specified block) by timer.

        const self = this;
        floating_full_screen_messenger = self;

        this.background = 'rgba(98, 117, 239, 0.4)';
        this.background_z_index = '100';
        this.background_font_color = 'white';
        this.background_style =
            'position: absolute;' +
            'display: flex;' +
            'align-items: center;' +
            'justify-content: center;' +
            'top: 0;' +
            'left: 0;' +
            'right: 0;' +
            'bottom: 0;' +
            'z-index: '+ self.background_z_index +' ;' +
            'text-align: center;' +
            'color: '+ self.background_font_color +';' +
            'background: '+ self.background + ';';

        this.preloader_img_width = '4rem';
        this.preloader_img_height = '4rem';
        this.preloader_img_style = 'width: '+ self.preloader_img_width +';height: '+ self.preloader_img_height +';';

        this.preloader_wrapper_style =
            'display: block;' +
            'padding: 0 auto;' +
            // 'position: fixed;' +
            // 'top: 50%;' +
            // 'left: 50%;' +
            // 'transform: translate(-50%, -50%);' +
            'text-align: center;';

        this.message_style = 'font-size: 4rem%;margin-top: 0.5rem;color: white;';
        this.tip_style = 'font-size: 0.7rem;color: white;';
        this.tip_indent_style = {'margin-top': '1rem'};
        this.return_button_style =
            'margin-top: 0.5rem;' +
            'padding: 0.5rem;' +
            'border-radius: 0.2rem;' +
            'border: 1px solid white;' +
            'color: white;';

        this.return_button_text = 'Вернуться';
        this.blur_style =  {'filter': 'blur(0.5rem)', '-webkit-filter': 'blur(0.5rem)'};

        this.message_container_class = 'js-full-screen-message';
        this.message_img_container_class = 'js-full-screen-message-img';
        this.message_text_container_class = 'js-full-screen-message-text';
        this.tip_message_container_class = 'js-full-screen-tip-message-text';
        this.return_button_class = 'js-return-btn';
        this.blur_container_class = 'js-blur';

        this.message = (
            $('<div/>', {
                class: self.message_container_class,
                style: self.background_style
            }).append(
                $('<div/>',{
                    class: self.message_img_container_class,
                    style: self.preloader_wrapper_style
                }).append(
                    $('<img>', {
                        style: self.preloader_img_style,
                        src: ''
                    })
                ).append(
                    $('<div/>',{
                        class: self.message_text_container_class,
                        style: self.message_style
                    })
                ).append(
                    $('<div/>',{
                        class: self.tip_message_container_class,
                        style: self.tip_style
                    })
                )
            )
        );

        this.return_button = (
            $('<button/>',{
                class: self.return_button_class,
                style: self.return_button_style,
                html: self.return_button_text
            })
        );

        this.showTimeOutMessage = function(
            container,
            icon='',
            text='',
            time_out=600,
            animation='slow',
            callback=null) {

            // Method for displaying a timeout message.

            let msg_container = $(container);

            self.message.find('.' + self.message_text_container_class).text(text);
            self.message.find('img').attr('src', icon);

            msg_container.append(self.message).fadeIn(animation);
            setBlur(msg_container);

            $.when(
                setTimeout(function() {
                    setBlur(msg_container, '');
                    self.message.remove();
                }, time_out)
            ).done(function (){
                if(callback){
                    setTimeout(function() {
                        callback(msg_container);
                    }, time_out)
                }
            })
        };

        this.preloaderMessage = function (
            container,
            main,
            done,
            icon='',
            text='',
            icon_on_fail='',
            text_on_fail='',
            animation='slow',
            timeOut=200) {

            // Method for displaying a message on completion of operations in the main callback and execution
            // of operations in the done callback.

            let msg_container = $(container);

            self.message.find('.' + self.message_text_container_class).text(text);
            self.message.find('img').attr('src', icon);

            msg_container.append(self.message).fadeIn(animation);
            setBlur(msg_container);

            setTimeout(function () {
                $.when(main).done(function (response){
                    self.message.remove();
                    done(response);
                }).fail(function (response){
                    self.addSimpleMessage(container, icon_on_fail, text_on_fail, animation)
                })
            }, timeOut);
        };

        this.addSimpleMessage = function (
            container,
            icon='',
            text='',
            animation='slow') {

            let msg_container = $(container);

            self.message.find('.' + self.message_img_container_class).append(self.return_button);
            self.message.find('.' + self.message_text_container_class).text(text);
            self.message.find('img').attr('src', icon);
            msg_container.append(self.message).fadeIn(animation);

            setBlur(msg_container);

            self.return_button.click(function () {
                setBlur(msg_container, '');
                self.message.remove();
            })
        };

        this.setTipMessage = function (text) {
            // Method for setting tooltip text to message.

            self.message.find('.' + self.tip_message_container_class).css(self.tip_indent_style).text(text);
        };

        function setBlur(parent_container, value=self.blur_style) {
            // Function to add container style blur.

            parent_container.find('.' + self.blur_container_class).css(value);
        }
    };
}