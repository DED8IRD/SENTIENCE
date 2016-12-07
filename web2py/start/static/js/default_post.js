/**
 * Created by DED8IRD on 12/4/2016.
 */
// This is the js for the default/post.html view

var app = function() {

    var self = {};

    Vue.config.silent = false; // show all warnings

    // Extends an array
    self.extend = function(a, b) {
        for (var i = 0; i < b.length; i++) {
            a.push(b[i]);
        }
    };

    self.view_post = function () {
        $.getJSON(post_url,
            function (data) {
                self.vue.post=data.post;
                formatTimeStamp(data.post);
                self.vue.comments=data.comments;
                formatTimeStamps(data.comments);
                self.vue.logged_in=data.logged_in;
            });
    };

    self.add_comment_button = function () {
        // The button to add a post has been pressed.
        if(self.vue.logged_in) {
            self.vue.is_adding_comment = !self.vue.is_adding_comment;
        }
    };

    self.add_comment = function () {
        // The submit button to add a post has been added.
        $.post(add_comment_url,
            {
                comment_content: self.vue.form_comment_content
            },
            function (data) {
                $.web2py.enableElement($("#post-button"));
                formatTimeStamp(data.comment);
                self.vue.comments.push(data.comment);
                self.vue.is_adding_comment = !self.vue.is_adding_comment;
                self.vue.form_comment_content = "";
            });
    };

    self.edit_comment_button = function(comment_id, comment_content) {
        self.vue.editing_comment = comment_id;
        if (comment_content) {
            self.vue.form_edit_comment_content = comment_content;
        }
    };

    self.edit_comment = function(comment_id, comment_index) {
        // The submit button to add a post has been added.
        $.post(edit_comment_url,
            {
                comment_id: comment_id,
                comment_content: self.vue.form_edit_comment_content
            },
            function (data) {
                if (data == "no")
                    return;
                comment = self.vue.comments[comment_index];
                comment.comment_content = self.vue.form_edit_comment_content;
                comment.updated_on = data;
                comment.updated = true;
            });
    };

    self.delete_comment = function(comment_id) {
        $.post(del_comment_url,
            {
                comment_id: comment_id
            },
            function (data) {
                if (data == "no")
                    return;
                var idx = null;
                for (var i = 0; i < self.vue.comments.length; i++) {
                    if (self.vue.comments[i].id === comment_id) {
                        // If I set this to i, it won't work, as the if below will
                        // return false for items in first position.
                        idx = i + 1;
                        break;
                    }
                }
                if (idx) {
                    self.vue.comments.splice(idx - 1, 1);
                }
            }
        )
    };

    self.vote = function(p_id, index, value) {
        $.post(vote_url,
        {
            post_id: p_id,
            vote_value: parseInt(value, 10)
        },
        function (data) {
            if (data.success == "no")
                return;
            post = self.vue.post;
            post.upvotes = data.count;
            post.my_vote = (data.success == "vote")? value: 0;
        });
    };

    self.vue = new Vue({
        el: "#vue-comment-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            post: null,
            comments: [],
            is_adding_comment: false,
            editing_comment: -1,
            logged_in: false,
            has_more: false,
            form_comment_content: null,
            form_edit_comment_content: null,
            infini_scroll_enabled: false,
            gen_img_url: null
        },
        methods: {
            view_post: self.view_post,
            add_comment_button: self.add_comment_button,
            add_comment: self.add_comment,
            edit_comment_button: self.edit_comment_button,
            edit_comment: self.edit_comment,
            delete_comment: self.delete_comment,
            vote: self.vote
        }

    });

    self.view_post();
    setTimeout(function(){$('#vue-comment-div').show();}, 100);

    return self;
};

var COMMENTAPP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){COMMENTAPP = app();});

