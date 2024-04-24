$(document).ready(function(){
    // 检查是否已经保存了登录信息
    if(localStorage.getItem('remember') === 'true'){
      $('input[name="email"]').val(localStorage.getItem('email'));
      $('input[name="password"]').val(localStorage.getItem('password')); // 密码应该经过加密
      $('input[name="remember-me"]').prop('checked', true);
    }

    // 表单提交处理器
    $('.login100-form').on('submit', function(){
      var rememberMeChecked = $('input[name="remember-me"]').is(':checked');
      var email = $('input[name="email"]').val();
      var password = $('input[name="password"]').val();
      if(rememberMeChecked){
        localStorage.setItem('email', email);
        localStorage.setItem('password', password);
        localStorage.setItem('remember', 'true');
      } else {
        localStorage.removeItem('email');
        localStorage.removeItem('password');
        localStorage.removeItem('remember');
      }
    });
  });