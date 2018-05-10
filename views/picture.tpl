<!doctype html>
<html lang="en">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>照相</title>
<link rel="stylesheet" href="../css/bootstrap.min.css">
<link rel="stylesheet" href="../css/styles.css">

<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js">
<script src="../js/bootstrap.min.js"></script>

<script type="text/javascript">
    $(document).ready(function(){
        $("button#take_pic").click(function(){
            $.ajax({
                type: 'GET',
                url: 'take_picture',
                success: function(data) {
                    $("img#picture").attr('src', data);
                }
            });
        });
        $("button#take_video").click(function(){
            $("video#video_display").attr('src', '');
            $("p#video_taking").html("Taking video for 1 minute. Please wait...")
            $.ajax({
                type: 'GET',
                url: 'take_video',
                success: function(data) {
                    $("p#video_taking").html("")
                    $("video#video_display").attr('src', data);
                }
            });
        });
    });
</script>
</head>

<body>
<div id = "background" style="font-size: 1.5em; font-weight: bold;">


    <div style="text-align: center; padding-top: 5.0em;">
        <button id="take_pic" type="button" class="btn btn-primary" style="font-size:2em;">
            Take a picture!
        </button>
        <br/>
        <img id="picture" src="" width="100%">
    </div>
    <div style="text-align: center; padding-top: 5.0em;">
        <button id="take_video" type="button" class="btn btn-primary" style="font-size:2em;">
            Take a video!
        </button>
        <br/><br/>
        <p id="video_taking"></p>
        <video id="video_display" width="100%" src="" controls>
            Your browser does not support HTML5 video.
        </video>
    </div>
</div>
</body>
</html>
