function binarySearch(lst, string, start, end){
  if(start > end) return [];

  let mid = Math.floor((start+end)/2);

  if(lst[mid] === string) return [lst[mid]];

  if(lst[mid] > string){
    return binarySearch(lst, string, start, mid-1);
  }
  else{
    return binarySearch(lst, string, mid+1, end);
  }
}

const stocks = ['BRK.B', 'TSM', 'V', 'AAPL', 'GOOG', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'TSLA', 'META', 'LLY', 'JNJ', 'JPM', 'BK', 'MA', 'NVO', 'MA', 'UNH', 'ORCL', 'BHP', 'CVX', 'ASML', 'ABBV', 'BAC', 'SHEL', 'CSCO', 'NFLX', 'AMD', 'TBC', 'NKE', 'SAP', 'DHR', 'DIS', 'WFC', 'VZ', 'RTX', 'MS', 'BMY', 'QCOM', 'BA'].sort(); // fill later

$(document).ready(function(){
    $("#search").focus(function() {
      $(".search-box").addClass("border-searching");
      $(".search-icon").addClass("si-rotate");
    });
    $("#search").blur(function() {
      $(".search-box").removeClass("border-searching");
      $(".search-icon").removeClass("si-rotate");
    });

    const socket = io();

    socket.on('connect', ()=>{
      console.log('Search is connected');
    });

    $('#search').keyup((e)=>{
      $('#stock-list').html('');

      const symbol = e.target.value;
      
      const results = binarySearch(stocks, symbol.toUpperCase(), 0, stocks.length-1);

      results.forEach(element => {
        const item = document.createElement('li');

        item.innerText = element;
        item.classList.add('searchedStock');

        
        socket.emit('hello', {'symbol': element}, (res)=>{
          const price = document.createElement('p');
          price.innerText = `Stock price: ${res.price}`;
          item.append(price);

          
          const button = document.createElement('button');
          button.innerText = 'Learn More';
          button.classList.add('search-button');
          item.append(button);
        });

        $('#stock-list').append(item);
      });

    })
});