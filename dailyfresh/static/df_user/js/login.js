/**
 * Created by python on 19-10-28.
 */

;$(function () {

    var error_name = false;

    $('#user_name').blur(function () {
        check_user_name();

    });

    function check_user_name(){
		var len = $('#user_name').val().length;
		if(len<5||len>20)
		{
			$('#user_name').next().html('用户名不存在')
			$('#user_name').next().show();
			error_name = true;
		}
		else
		{
			$('#user_name').next().hide();

			var param = $('#submit_form').serialize();
			var url ='/user/register_exist/';
			$.get(url, param, function (data) {
				var result = data;
				if(result.count == 0){
					$('#user_name').next().html('用户名不存在');
					$('#user_name').next().show();
					error_name = true;
				}else{
					error_name = false;
				}

            });



		}
	}


    $('#submit_form').submit(function() {
		check_user_name();
		if(error_name == false)
		{
		    var url = '/user/login_handle/';

		    var param = $('#submit_form').serialize();
            $.get(url, param, function (data) {
				var result = data;
				var return_url = result.url;
				console.log('return_url:'+return_url)
				if(return_url == ''){
					$('#user_name').next().html('密码错误');
					$('#user_name').next().show();
				}else{
					error_name = false;
					$(location).attr('href', return_url);
				}

            });

		}

		return false;


	});

});
