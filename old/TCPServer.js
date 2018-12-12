var net = require('net');
// 5000번 포트로 서버Start

var server = net.createServer(function(socket){
    console.log('connection...');
    socket.setEncoding('utf8'); // utf8 인코딩
    socket.write("안녕하세요, 지금부터 글자를 입력하시고 종료하시려면 quit을 입력하세요");    

    // 클라이언트로부터 quit 문자열 수신시 종료처리
    socket.on('data', function(data){
        console.log('recv data: '+ data);
      
        if(data.trim().toLowerCase() == 'quit'){
            socket.write('>>>>>클라이언트와 연결을 종료합니다.');
            return socket.end();
        }
        socket.write('>>>>'+data);
    });
    socket.on('end', function(){ 
        console.log('client connection disconnected...');
    });

    socket.on('error',function(err){
      console.log('Client 연결이 quit이 아닌 방법으로 끊겼습니다.')
    })
}).listen(5000);





// const net = require('net')

// const server = net.createServer(socket=>{
//   console.log(socket.address().address + " connected!")
//   socket.on('data', data=>{
//     console.log('rcv : ' + data)
//   })

//   socket.on('close', data=>{
//     console.log("client disconnected!")
//   })

//   socket.write('welcome to server!')
// })

// server.on('error',err=>{
//   console.log('err : ' + err)
// })

// server.listen(5000, ()=>{
//   console.log('listening 5000')
// })