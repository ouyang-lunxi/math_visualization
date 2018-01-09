String.prototype.format= function(){
	let args = arguments;
	return this.replace(/\{(\d+)\}/g,function(s,i){
 		return args[i];
	});
}

function rowConvert(rows){
	rows.sort((a,b)=>{
		return a.x[0] - b.x[0];
	});
	for(let i = 1;i<rows.length;i++){
		rows[i].y = rows[i - 1].y + rows[i].y;
	};
}

function subjectRender(subjectName,itemName,index){
	let interval = binInterval[itemName];
	let subInterval = interval / 10;
	let filename = "csv/{0}/{1}_{0}.csv".format(itemName,subjectName);
	$.ajax({
		url:filename,
		dataType:"text",
		success:data=>{
			let ds = new DataSet({
				state:{
					x:interval == 0.1 ? "0.0,0.1" : "0,50"
				}
			});

			let dv_1 = ds.createView("total")
			let dv_2 = ds.createView("sub")
			dv_1.source(data,{
				type:"csv",
			});
			dv_2.source(data,{
				type:"csv",
			});

			dv_1.transform({
				type:"bin.histogram",
				field:"head",
				binWidth:interval,
				as:["x","y"]
			});

			dv_2.transform({
				type:"filter",
				callback(row){
					let u = parseFloat(ds.state.x.split(",")[0]);
					let d = parseFloat(ds.state.x.split(",")[1]);
					return parseFloat((row.head)) < d && parseFloat((row.head)) >= u;
				}
			});

			dv_2.transform({
				type:"bin.histogram",
				field:"head",
				binWidth:subInterval,
				as:["x","y"]
			});

			// 观看时长算累加和
			if (itemName == "learnTime"){
				dv_1.transform({
					type: 'sort',
					callback(a, b) { // 排序依据，和原生js的排序callback一致
						return a.x[0] - b.x[0];
					}
				});
				dv_1.transform({
					type: 'map',
					callback(row) { // 加工数据后返回新的一行，默认返回行数据本身
						let ix = dv_1.rows.indexOf(row);
						if (ix){
							row.y += dv_1.rows[ix - 1].y;
						}
						return row;
					}
				});
				dv_2.transform({
					type: 'sort',
					callback(a, b) { // 排序依据，和原生js的排序callback一致
						return a.x[0] - b.x[0];
					}
				});
				dv_2.transform({
					type: 'map',
					callback(row) { // 加工数据后返回新的一行，默认返回行数据本身
						let ix = dv_2.rows.indexOf(row);
						if (ix){
							row.y += dv_2.rows[ix - 1].y;
						}
						return row;
					}
				});
			};
			
			let chart = new G2.Chart({
				container:"c{0}1".format(index + 1),
				forceFit: true,
				heitht:300
			});
			chart.tooltip({
				crosshairs: false,
				inPlot: false,
				position: 'top'
			});
			chart.source(dv_1,{
				x:{
					tickInterval:interval,
					formatter:val=>{
						if(val instanceof Array){
							val[0] = parseFloat(val[0]).toFixed(1);
							val[1] = parseFloat(val[1]).toFixed(1);
						}
						return val;
					}
				},
				y:{
					min:0,
				}
			});

			chart.on("tooltip:change",function(evt){
				const items = evt.items || [];
				if (items[0]){
					ds.setState("x",items[0].title);
				}
			});

			chart.interval().position("x*y");
			chart.render();

			let chart_2 = new G2.Chart({
				container:"c{0}2".format(index+ 1),
				forceFit: true,
				heitht:300
			});
			chart_2.tooltip({
				crosshairs: false,
				inPlot: false,
				position: 'top'
			});
			chart_2.source(dv_2,{
				x:{
					tickInterval:subInterval,
					formatter:val=>{
						if(val instanceof Array){
							val[0] = parseFloat(val[0]).toFixed(2);
							val[1] = parseFloat(val[1]).toFixed(2);
						}
						return val;
					}
				},
				y:{
					min:0,
				}
			});
			chart_2.interval().position("x*y");
			chart_2.render();
			console.log(chart_2.data);
		}
	});



};

function allSubjectRender(){
	console.log($(itemSelect).val());
	if($(itemSelect).val()){
			let val = $(itemSelect).find('option:selected').val();
			for(let i=0;i<5;i++){
				$("#c{0}1".format(i + 1)).empty();
				$("#c{0}2".format(i + 1)).empty();
				subjectRender(subjectNames[i],val,i);
			}
	}
}

items = new Array()
items["learnTime"] = "观看时长分布"
items["clickVideoExit"] = "退出时间点分布"
items["dragVideoForward"] = "向前拖拽行为分布"
items["dragVideoForward5"] = "向前拖拽5s行为分布"
items["dragVideoForward0"] = "向前拖拽5-10s行为分布"
items["dragVideoBackward"] = "向后拖拽行为分布"
items["dragVideoBackward5"] = "向后拖拽5s行为分布"
items["dragVideoBackward0"] = "向后拖拽5-10s行为分布"
items["dragVideoForwardDuration"] = "向前拖拽时长分布"
items["dragVideoBackwardDuration"] = "向后拖拽时长分布"

binInterval = new Array()
binInterval["learnTime"] = 0.1
binInterval["clickVideoExit"] = 0.1
binInterval["dragVideoForward"] = 0.1
binInterval["dragVideoForward5"] = 0.1
binInterval["dragVideoForward0"] = 0.1
binInterval["dragVideoBackward"] = 0.1
binInterval["dragVideoBackward5"] = 0.1
binInterval["dragVideoBackward0"] = 0.1
binInterval["dragVideoForwardDuration"] = 50
binInterval["dragVideoBackwardDuration"] = 50


subjectNames = new Array("点到圆的距离","对数的定义(上)","对数的化简与求值","集合的基本运算-交集","平方根")

$(document).ready(function(){
	for (itemName in items){
		$("#itemSelect").append("<option value={0}>{1}</option>".format(itemName,items[itemName]));
	};
	$("#itemSelect option[value='itemSelect']").attr("selected",true);
	$("#itemSelect").on("change",function (){
		console.log($(itemSelect).val());
		if($(this).val()){
				let val = $(this).find('option:selected').val();
				for(let i=0;i<5;i++){
					$("#c{0}1".format(i + 1)).empty();
					$("#c{0}2".format(i + 1)).empty();
					subjectRender(subjectNames[i],val,i);
				}
		}
	});
	$("#itemSelect").trigger("change");
});


