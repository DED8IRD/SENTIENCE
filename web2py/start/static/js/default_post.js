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
                self.vue.comments.unshift(data.comment);
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
            delete_comment: self.delete_comment
        }

    });

    self.view_post();
    $("#vue-comment-div").show();
    return self;
};


/*
  Utility functions for timestamp formatting
 */
function readableTime(time) {
    var readable = time.split(":");
    var hour = parseInt(readable[0], 10);
    var min = readable[1];
    var sec = readable[2];
    var period = (hour < 12)? "AM": "PM";
    hour = hour % 12;
    hour = (hour == 0)? 12: hour;
    return hour+":"+min+":"+sec+" "+period;
}

function magicDateFunction(datetime) {
    var arr = datetime.split(" ");
    var date = arr[0].split("-");
    var year = date[0];
    var month = parseInt(date[1], 10);
    var day = parseInt(date[2], 10);

    return new Date(month+"/"+day+"/"+year+" "+readableTime(arr[1])+" UTC");
}

// [ "Thu", "Dec", "01", "2016", "23:35:11", "GMT-0800", "(Pacific", "Standard", "Time)" ]
function formatTimeStamp(comment) {
    var timestamp = magicDateFunction(comment.created_on);
    var datetime = timestamp.toString().split(" ");

    var month = datetime[1];
    var day = parseInt(datetime[2], 10);
    var year = parseInt(datetime[3], 10);
    var time = readableTime(datetime[4]);
    var readable = month+" "+day+", "+year+ " at " + time;
    comment.date_tooltip = readable;

    var now = new Date();
    var timeDiff = [1000, 60, 60, 24];
    var times = [now-timestamp];
    for (var i = 0; i < timeDiff.length; ++i) {
        times[i+1] = times[i] / timeDiff[i];
    }
    for (var i = 1; i < times.length; ++i) {
        times[i] = Math.floor(times[i]);
    }
    var timeStringsSingular = ["1 minute ago", "1 hour ago", "Yesterday at " + time];
    var timeStrings = [times[2] + " minutes ago", times[3] + " hours ago", readable];
    readable = times[1] + ((times[1] == 1)? " second ago":" seconds ago");
    for (var i = 0; i < timeStrings.length; ++i)
        if (times[i+2] == 1) {
            readable = timeStringsSingular[i];
        } else if (times[i+2] > 0) {
            readable = timeStrings[i];
        }

    comment.date_readable = readable;
}

function formatTimeStamps(comments) {
    for (var i = 0; i < comments.length; ++i){
        formatTimeStamp(comments[i]);
    }
}

var COMMENTAPP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){COMMENTAPP = app();});

