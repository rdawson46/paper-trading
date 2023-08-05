document.addEventListener('DOMContentLoaded', async()=>{
    const header = document.getElementById('header');
    const user = header.dataset.user;
    const symbol = header.dataset.stock;

    console.log(user)
    console.log(symbol)

    const response = await fetch(`/${user}/stock/${symbol}/charting`)
    
    if (!response.ok){
        throw new Error('Response was not ok');
    }

    const data = await response.json();

    console.log(data)
    
    // data = [[1,5], [2,6],[3,7]]
    const xvals = data.xvals
    const yvals = data.yvals
    
    // data.forEach(element => {
    //     xvals.push(element[0]);
    //     yvals.push(element[1]);
    // });
    
    console.log(xvals)
    console.log(yvals)
    
    const myChart = new Chart('myChart',{
        type: 'line',
        data: {
            labels: xvals,
            datasets: [{
                backgroundColor:"rgba(213, 56, 103, 0.3)",
                borderColor: "rgba(213, 56, 103, 1.0)",
                data: yvals
            }]
        },
        options: {}
    });

});
