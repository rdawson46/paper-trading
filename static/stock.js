document.addEventListener('DOMContentLoaded', async()=>{
    const header = document.getElementById('header');
    const user = header.dataset.user;
    const symbol = header.dataset.stock;

    const response = await fetch(`/${user}/stock/${symbol}/charting`)
    
    if (!response.ok){
        throw new Error('Response was not ok');
    }

    const data = await response.json();
    
    let xvals = data.xvals
    let yvals = data.yvals

    xvals = xvals.map(elem=>{return elem.slice(5)})

    const myChart = new Chart('myChart',{
        type: 'line',
        data: {
            labels: xvals,
            datasets: [{
                label: 'Price',
                backgroundColor:"rgba(213, 56, 103, 0.3)",
                borderColor: "rgba(213, 56, 103, 1.0)",
                data: yvals
            }]
        },
        options: {}
    });

});
