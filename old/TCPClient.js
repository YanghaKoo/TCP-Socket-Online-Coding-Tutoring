var net = require('net');

process.stdin.resume();         // 표준입력처리(입력받을수 있도록 변경)
//process.stdin.setEncoding('utf8')

var client = net.connect(
        { host:'localhost', port:5000 },
        function(){
            console.log('connection!');
        }); 

// 서버에서 data가 왔을때 하는 이벤트
client.on('data', function(data){       // 서버로부터 데이터 수신시 콘솔에 출력
    console.log(data.toString());
});


// quit 쳐서 이벤트가 종료되었을때 발생
client.on('end', function(data){
    //console.log(data.toString()); // end가 되는데 data를 왜 찍지? 애초에 data가 있나?
    console.log("end event")
});

// end 다음에 close로 간다
client.on('close', function(){
    console.log('close client....');
});

// error 발생 시 
client.on('error',function(err){
    console.log('시발')
  })

// 사용자가 콘솔에서 텍스트를 입력하였을 경우 write함수로 서버에 전송
process.stdin.on('data', function(data){
    if(data.toString().trim().toLowerCase() == 'quit'){
        console.log('request disconnect');
        client.write(data);
        process.stdin.end();
    }else{
        // process.stdout.write(data)  // 이건 클라이언트 콘솔에 내가 입력한걸 찍는거임
        client.write(data);     
    }
})


// const net = require('net')

// const socket = net.connect({port : 5000})
// socket.on('connect', ()=>{
//   console.log('connected to server!')

//   setInterval(()=>{
//     socket.write('banana hong!')
//   },1000)
// })

// socket.on('data',chunk=>{
//   console.log('recv : ' + chunk)
// })

// socket.on('end',()=>{
//   console.log('disconnected')
// })

// socket.on('error', err =>{
//   console.log(err)
// })

// socket.on('timeout', ()=>{
//   console.log('connection timeoutc')
// })