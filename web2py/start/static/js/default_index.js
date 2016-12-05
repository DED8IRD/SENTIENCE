// This is the js for the default/index.html view

var app = function() {
    // Constants:
    var INITIAL_POST_COUNT = 0;
    var ADDITIONAL_POST_LOAD = 1;

    var self = {};

    Vue.config.silent = false; // show all warnings

    // Extends an array
    self.extend = function(a, b) {
        for (var i = 0; i < b.length; i++) {
            a.push(b[i]);
        }
    };

    function get_posts_url(start_idx, end_idx) {
        var pp = {
            start_idx: start_idx,
            end_idx: end_idx
        };
        return posts_url + "?&" + $.param(pp);
    }

    self.get_posts = function () {
        $.getJSON(get_posts_url(0, INITIAL_POST_COUNT), function (data) {
            self.vue.posts = data.posts;
            self.vue.has_more = data.has_more;
            self.vue.logged_in = data.logged_in;
            self.infini_scroll();
        })
    };

    self.get_more = function () {
        var num_posts = self.vue.posts.length;
        $.getJSON(get_posts_url(num_posts, num_posts + ADDITIONAL_POST_LOAD), function (data) {
            self.vue.has_more = data.has_more;
            self.extend(self.vue.posts, data.posts);
            self.vue.infini_scroll_enabled = true;
        });
    };

    self.add_post_button = function () {
        // The button to add a post has been pressed.
        self.vue.is_adding_post = !self.vue.is_adding_post;
    };

    self.add_post = function () {
        // The submit button to add a post has been added.
        $.post(add_post_url,
            {
                post_content: self.vue.form_post_content
            },
            function (data) {
                $.web2py.enableElement($("#post-button"));
                self.vue.posts.unshift(data.post);
            });
    };

    self.edit_post_button = function(post_id, post_content) {
        self.vue.editing_post = post_id;
        if (post_content) {
            self.vue.form_edit_post_content = post_content;
        }
    }

    self.edit_post = function(post_id, post_index) {
        // The submit button to add a post has been added.
        $.post(edit_post_url,
            {
                post_id: post_id,
                post_content: self.vue.form_edit_post_content,
            },
            function (data) {
                if (data == "no")
                    return;
                post = self.vue.posts[post_index]
                post.post_content = self.vue.form_edit_post_content
                post.updated_on = data
                post.updated = true
            });
    }

    self.delete_post = function(post_id) {
        $.post(del_post_url,
            {
                post_id: post_id
            },
            function (data) {
                if (data == "no")
                    return;
                var idx = null;
                for (var i = 0; i < self.vue.posts.length; i++) {
                    if (self.vue.posts[i].id === post_id) {
                        // If I set this to i, it won't work, as the if below will
                        // return false for items in first position.
                        idx = i + 1;
                        break;
                    }
                }
                if (idx) {
                    self.vue.posts.splice(idx - 1, 1);
                }
            }
        )
    };

    self.infini_scroll = function() {
        var bottom = $(document).height()-$(window).height() - $(window).scrollTop();
        var check = bottom < 50;
        if (check && self.vue.has_more) {
            if (self.vue.infini_scroll_enabled) {
                self.vue.infini_scroll_enabled = false;
                self.get_more();
            }
            setTimeout(function(){self.infini_scroll();}, 500);
        }
    };

    self.generate_post = function () {
        // The submit button to add a post has been added.
        $.get(generate_post_url,
            function (data) {
                self.vue.posts.unshift(data.post);
            });
    };

    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            posts: [],
            is_adding_post: false,
            editing_post: -1,
            logged_in: false,
            has_more: false,
            form_post_content: null,
            form_edit_post_content: null,
            infini_scroll_enabled: false,
            gen_img_url: null
        },
        methods: {
            get_more: self.get_more,
            add_post_button: self.add_post_button,
            add_post: self.add_post,
            edit_post_button: self.edit_post_button,
            edit_post: self.edit_post,
            delete_post: self.delete_post,
            infini_scroll: self.infini_scroll,
            generate_post: self.generate_post
        }

    });


    $(window).scroll(self.infini_scroll);
    $(window).resize(self.infini_scroll);

    self.vue.infini_scroll_enabled = true;

    self.get_posts();
    $("#vue-div").show();

    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});
