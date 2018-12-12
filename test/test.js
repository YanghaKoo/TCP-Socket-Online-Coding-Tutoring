function removeDuplicate(arr){
  var exists ={},
      outArr = [], 
      elm;

  for(var i =0; i<arr.length; i++){
    elm = arr[i];
    if(!exists[elm]){
      outArr.push(elm);
      exists[elm] = true;
   }
  }
  return outArr;
} 

console.dir(removeDuplicate([1,10,4,5,11)]) 