function siteTime(){	
	var seconds = 1000 
	var minutes = seconds * 60
	var hours = minutes * 60
	var days = hours * 24
	//var years = days * 365
	
	var today = new Date()
	var todayYear = today.getFullYear()
	var todayMonth = today.getMonth()
	var todayDate = today.getDate()
	var todayHour = today.getHours()
	var todayMinute = today.getMinutes()
	var todaySecond = today.getSeconds()
	var todayMillisecond = today.getMilliseconds()
	
	var t1 = Date.UTC(2007,10,5,15,15,0)
	var t2 = Date.UTC(todayYear,todayMonth,todayDate,todayHour,todayMinute,todaySecond,todayMillisecond)
	var diff = t2-t1
	var diffDays = Math.floor(diff/days)
	var diffHours = Math.floor((diff-diffDays*days)/hours)
	var diffMinutes = Math.floor((diff-diffDays*days-diffHours*hours)/minutes)
	var diffSeconds = Math.floor((diff-diffDays*days-diffHours*hours-diffMinutes*minutes)/seconds)
	var diffMilliseconds = Math.floor((diff-diffDays*days-diffHours*hours-diffMinutes*minutes-diffSeconds*1000)/1)
	if (diffMilliseconds < 10){
		diffMilliseconds = "00"+diffMilliseconds
	}else if (diffMilliseconds < 100){
		diffMilliseconds = "0"+diffMilliseconds	
	}
	document.getElementById('sitetime').innerHTML="ppCat.Ing 已经建立并运行了 "+diffDays+" 天 "+diffHours+" 小时 "+diffMinutes+" 分钟 "+diffSeconds+"."+diffMilliseconds+" 秒。"
	t=setTimeout('siteTime()',10)
}