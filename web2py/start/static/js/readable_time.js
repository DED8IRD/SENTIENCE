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
function formatTimeStamp(post) {
    var timestamp = magicDateFunction(post.created_on);
    var datetime = timestamp.toString().split(" ");

    var month = datetime[1];
    var day = parseInt(datetime[2], 10);
    var year = parseInt(datetime[3], 10);
    var time = readableTime(datetime[4]);
    var readable = month+" "+day+", "+year+ " at " + time;
    post.date_tooltip = readable;

    var now = new Date();
    var timeDiff = [1000, 60, 60, 24];
    var times = [now-timestamp];
    for (var i = 0; i < timeDiff.length; ++i) {
        times[i+1] = times[i] / timeDiff[i];
    }
    for (i = 1; i < times.length; ++i) {
        times[i] = Math.floor(times[i]);
    }
    var timeStringsSingular = ["1 minute ago", "1 hour ago", "Yesterday at " + time];
    var timeStrings = [times[2] + " minutes ago", times[3] + " hours ago", readable];
    readable = ((times[1] < 6)? "Just now":times[1] + " seconds ago");
    for (i = 0; i < timeStrings.length; ++i)
        if (times[i+2] == 1) {
            readable = timeStringsSingular[i];
        } else if (times[i+2] > 0) {
            readable = timeStrings[i];
        }

    post.date_readable = readable;
}

function formatTimeStamps(list) {
    for (var i = 0; i < list.length; ++i) {
        formatTimeStamp(list[i]);
    }
}