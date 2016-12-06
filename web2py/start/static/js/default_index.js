// This is the js for the default/index.html view

var app = function() {
    // Constants:
    var INITIAL_POST_COUNT = 0;
    var ADDITIONAL_POST_LOAD = 1;
    var INFINI_SCROLL_THRESHOLD = 100;

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
        $.getJSON(get_posts_url(0, INITIAL_POST_COUNT),
            function (data) {
                formatTimeStamps(data.posts);
                self.vue.posts = data.posts;
                self.vue.has_more = data.has_more;
                self.vue.logged_in = data.logged_in;
                self.infini_scroll();
            })
    };

    self.get_more = function () {
        var num_posts = self.vue.posts.length;
        $.getJSON(get_posts_url(num_posts, num_posts + ADDITIONAL_POST_LOAD),
            function (data) {
                self.vue.has_more = data.has_more;
                formatTimeStamps(data.posts);
                self.extend(self.vue.posts, data.posts);
                self.vue.infini_scroll_enabled = true;
            });
    };

    self.add_comment_button = function () {
        // The button to add a post has been pressed.
        self.vue.is_adding_comment = !self.vue.is_adding_comment;
    };

    self.add_comment = function () {
        // The submit button to add a post has been added.
        $.post(add_comment_url,
            {
                comment_content: self.vue.form_comment_content
            },
            function (data) {
                $.web2py.enableElement($("#post-button"));
                self.vue.posts.unshift(data.post);
            });
    };

    self.edit_comment_button = function(comment_id, comment_content) {
        self.vue.editing_comment = comment_id;
        if (comment_content) {
            self.vue.form_edit_comment_content = comment_content;
        }
    }

    self.edit_comment = function(comment_id, comment_index) {
        // The submit button to add a post has been added.
        $.post(edit_comment_url,
            {
                comment_id: comment_id,
                comment_content: self.vue.form_edit_comment_content,
            },
            function (data) {
                if (data == "no")
                    return;
                post = self.vue.posts[post_index];
                post.post_content = self.vue.form_edit_comment_content;
                post.updated_on = data;
                post.updated = true;
            });
    }

    self.delete_comment = function(comment_id) {
        $.post(del_comment_url,
            {
                comment_id: comment_id
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
        var check = bottom < INFINI_SCROLL_THRESHOLD;
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
            is_adding_comment: false,
            editing_comment: -1,
            logged_in: false,
            has_more: false,
            form_comment_content: null,
            form_edit_comment_content: null,
            infini_scroll_enabled: false
        },
        methods: {
            get_more: self.get_more,
            add_comment_button: self.add_comment_button,
            add_comment: self.add_comment,
            edit_comment_button: self.edit_comment_button,
            edit_comment: self.edit_comment,
            delete_comment: self.delete_comment,
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


/*
  Utility functions for timestamp formatting
 */
function readableTime(time, seconds) {
    var readable = time.split(":");
    var hour = parseInt(readable[0], 10);
    var min = readable[1];
    var sec = readable[2];
    var period = (hour < 12)? "AM": "PM";
    hour = hour % 12;
    hour = (hour == 0)? 12: hour;
    return (seconds)? hour+":"+min+":"+sec+" "+period: hour+":"+min+period.toLowerCase();
}

function magicDateFunction(datetime) {
    var arr = datetime.split(" ");
    var date = arr[0].split("-");
    var year = date[0];
    var month = parseInt(date[1], 10);
    var day = parseInt(date[2], 10);

    return new Date(month+"/"+day+"/"+year+" "+readableTime(arr[1], true)+" UTC");
}

// [ "Thu", "Dec", "01", "2016", "23:35:11", "GMT-0800", "(Pacific", "Standard", "Time)" ]
function formatTimeStamp(post) {
    var timestamp = magicDateFunction(post.created_on);
    var datetime = timestamp.toString().split(" ");

    var months = ["January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"];
    var month = months[timestamp.getMonth()];
    var day = parseInt(datetime[2], 10);
    var year = parseInt(datetime[3], 10);
    var time = readableTime(datetime[4], false);
    var readable = month+" "+day+", "+year+ " at " + time;
    post.date_tooltip = readable;

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
    var timeStrings = [times[2] + " minutes ago", times[3] + " hours ago", month + " " + day];
    readable = times[1] + ((times[1] == 1)? " second ago":" seconds ago");
    for (var i = 0; i < timeStrings.length; ++i) {
        if (times[i + 2] == 1) {
            readable = timeStringsSingular[i];
        } else if (times[i + 2] > 0) {
            readable = timeStrings[i];
        }
    }
    if (year != parseInt((now.toString().split(" "))[3], 10)) {
        readable = month + " " + day + ", " + year
    }

    post.date_readable = readable;
}

function formatTimeStamps(posts) {
    for (var i = 0; i < posts.length; ++i){
        formatTimeStamp(posts[i]);
    }
}

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});
