/**
 * Created by python on 19-10-28.
 */
// 封装js公共方法
;$main_method = (function () {
    var main_object = {'ajax': ajax}

    function ajax(url,param){
        var result = $.get(url, param);
        alert(result.responseText)
        return result.responseText;
    }


    return main_object;

})();
