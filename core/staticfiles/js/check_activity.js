


const requestUserForActivity = JSON.parse(document.getElementById('json-request-user-for-activity').textContent);
console.log(requestUserForActivity.length, 'hrhrhrhr')


if (requestUserForActivity){
    var currSeconds, timer = 1
let isInitialTimer = true

function state(value){
    variable = value
    function changeState(arg){
        prevValue = variable
        variable = arg
        return { value: variable, changeState: changeState,
        prevValue: prevValue}
       }
    return  {value: variable, changeState: changeState,
       prevValue: null}
    }

let isAway = state(0)

function resetTimer() {
    clearInterval(timer);
    currSeconds = 1;
    timer = setInterval(startIdleTimer, 1000);
    isAway.value && (isAway = isAway.changeState(0))

}

// Define the events that
// would reset the timer
window.onload = resetTimer;
window.onmousemove = resetTimer;
window.onmousedown = resetTimer;
window.ontouchstart = resetTimer;
window.onclick = resetTimer;
window.onkeypress = resetTimer;
document.onkeydown = resetTimer;   // onkeypress is deprectaed
document.addEventListener('scroll', resetTimer, true);


function startIdleTimer() {
    currSeconds++;
    // console.log(currSeconds)
    // console.log(isAway.prevValue, isAway.value, '++++++++')
    if (isAway.prevValue && !isAway.value && (currSeconds == 3)){
        console.log('welcome back')
        isAway = isAway.changeState(0)
        sendUserActivity(true, 'online')
    }

    if (!isAway.value && currSeconds == 15 ){
        console.log('is_away')
        isAway = isAway.changeState(1)
        sendUserActivity(true, 'away')
    }
}

const userActivitySocket = new WebSocket(
    'ws://' + window.location.host
    + '/ws/user_activity/'
)

function sendUserActivity (isOnline, status) {
    userActivitySocket.send(JSON.stringify(
        {'status': status, 'is_online': isOnline,
        'time': new Date()
        }
    ))

}

userActivitySocket.onopen = () => {
    console.log('connected')
    sendUserActivity(true, 'online')
}

userActivitySocket.onmessage = (event) => {
    console.log('message')
    let data = JSON.parse(event.data)
    console.log(data, "datadatadatadatadatadatadatadata")


    let colorClass = data.status == 'online' ? 'text-lime-500'  : (data.status == 'offline')
    ? 'text-red-600' : 'text-yellow-500'
    if (data.is_activity && document.querySelector(`p[name=user-status-${data.user}]`)){
        
        document.querySelector(`p[name=user-status-${data.user}]`).className = colorClass
        document.querySelector(`p[name=user-status-${data.user}]`).innerHTML = data.status
    }
}

userActivitySocket.onclose = () => {
    console.log('close')
    sendUserActivity(false, 'offline')
}

}


