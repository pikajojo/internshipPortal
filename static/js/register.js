//测试引入成功
// 全部网页元素加载成功之后执行此功能

// 验证码按钮
function bindCode(){
    $("#captcha-btn").click(function(event){
        var $this = $(this);
        // 阻止默认提交
        event.preventDefault();
        var email = $("input[name='email']").val();

        // 使用ajax
        $.ajax({
            url:"/captcha/email?email="+email,
            method:"GET",
            success:function(result){
                console.log(result)
                var code = result['code']
                if (code == 200){
                    alert("Successfuly!! Verification code has been sent to your email! ")
                    var countdown = 5;
                    $this.off("click")
                    var timer = setInterval(function(){
                        $this.text(countdown);
                        countdown-=1;
                        if (countdown <= 0){
                            clearInterval(timer);
                            $this.text("Get Verfication Code");
                            bindCode();
                        }
                    }, 1000)

                } else {
                    console.log(result['message'])
                }
            },
            fail: function(error){console.log(error);},
        })

    });

}

/// 确认密码
function countdownheckCode(){
    $("#register-form").submit(function(event){
        event.preventDefault(); // 阻止表单默认提交行为

        var password = $("input[name='password']").val(); // 获取密码输入框的值
        var confirm_password = $("input[name='password_confirm']").val(); // 获取确认密码输入框的值

        // 检查密码和确认密码是否一致
        if(password !== confirm_password) {
            // 如果密码和确认密码不一致，给出提示并阻止表单提交
            alert("Password and confirm password do not match!");
            return;
        }
    });
}

$(function(){
    bindCode();
    countdownheckCode(); // 添加这一行，确保页面加载时调用 countdownheckCode 函数
});