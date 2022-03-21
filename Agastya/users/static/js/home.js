let rotation = 0;
let newFrame = false;
let topSpeed = 0.1;
let pageYDistance = 0;
let ClickCounter = 0;
let offsetWidth = 1300;
let offsetHeight = 2000;
let barClicked = false;
const totalPageHeight = document.body.scrollHeight - window.innerHeight;
let focused = false;
let val = 0.0;

//Animated Background - Canvas
let canvas = document.getElementById("myCanvas");
canvas.width = window.innerWidth + offsetWidth;
canvas.height = window.innerHeight + offsetHeight;
let ctx = canvas.getContext("2d");
let ctxEmpty = canvas.getContext("2d");
let canvasData = ctx.getImageData(0, 0, canvas.width, canvas.height);
//Animated Background - Point-Initialisation
var points = [{ x: -10, y: -10, targetx: -10, targety: -10, cooldown: 0, velocityX: 0, velocityY: 0, name:"00", distance: 0 }];
for(let count = 1; count <= 120; count++)
{
	const wx = Math.round(Math.random() * canvas.width);
	const wy = Math.round(Math.random() * 500);
	points.push({ x: wx, y: wy, targetx: wx, targety: wy, cooldown: 0, velocityX: wx, velocityY: wy, name: count.toString(), distance: 0 });
}
//Cursor Position-Object
let mousePos =
{
	x: -10,
	y: -10
};

//Global EventHandlers
document.onmousemove = onMouseMove;
window.addEventListener("scroll", onScroll);


window.requestAnimationFrame(loop);
function loop()
{
	draw();
	window.requestAnimationFrame(loop);
}

function draw()
{
	rescale(canvas, window.innerWidth, window.innerHeight, offsetWidth, offsetHeight);

	//Draw Background
	let grd = ctx.createRadialGradient(canvas.width*3, canvas.height* 3, 5, canvas.width*3, canvas.height *3, canvas.width * 3);
	grd.addColorStop(1, rgb(0, 0, 30));
	grd.addColorStop(0, rgb(0, 0, 66));
	ctx.fillStyle = grd;
	ctx.fillRect(0, 0, canvas.width, canvas.height);


	//Draw MouseCursor
	let pos = mousePos;
	let mouseGrd = ctx.createRadialGradient(pos.x + 1, pos.y + 1, 3, pos.x, pos.y, 30);
	ctx.beginPath();
	mouseGrd.addColorStop(0, rgb(7, 7, 70));
	mouseGrd.addColorStop(1, rgba(7, 7, 70, 0));
	ctx.fillStyle = mouseGrd;
	ctx.arc(pos.x, pos.y, 30, 0, 360, false);
	ctx.fill();


	//Draw lines between points
	var lines;
	var distances;
	var cursor;
	var closest1 = { distance: 1000 };
	var closest2 = { distance: 1000 };
	for (let item of points)
	{
		//Calculate Lines
		for (let innerItem of points)
		{
			let dis = getDistance(innerItem.x, innerItem.y, item.x, item.y);
			if (dis < 1000 && dis < (closest1.distance * 0.666666) && dis > 30)
			{
				innerItem.distance = getDistance(innerItem.x, innerItem.y, item.x, item.y);
				closest1 = innerItem;
			}
			else if (dis < 1000 && dis < (closest2.distance * 0.666666) && dis > 30)
			{
				innerItem.distance = getDistance(innerItem.x, innerItem.y, item.x, item.y);
				closest2 = innerItem;
			}
		}

		//Draw Lines
		ctx.beginPath();
		ctx.strokeStyle = rgb(35, 35, 115);
		ctx.moveTo(closest1.x, closest1.y);
		ctx.lineTo(item.x, item.y);
		ctx.stroke();
		ctx.lineTo(closest2.x, closest2.y);
		ctx.stroke();

		closest1.distance = 1000.0;
		closest2.distance = 1000.0;
	}

	//Draw points and move them around
	for (let item of points)
	{
		ctx.beginPath();
		var pointGrd = ctx.createRadialGradient(item.x - 1, item.y - 1, 1, item.x, item.y, 10);
		pointGrd.addColorStop(0, rgb(30, 30, 100));
		pointGrd.addColorStop(1, rgb(0, 0, 50));
		ctx.fillStyle = pointGrd;
		ctx.arc(item.x, item.y, 10, 0, 360, false);
		ctx.fill();
		ctx.strokeStyle = rgb(0, 0, 30);
		ctx.stroke();

		//Cooldown at 0 -> New Targets get set
		if (item.cooldown <= 0)
		{
			item.cooldown = Math.round(Math.random() * 200 + 100);

			if (item.targetx <= 20)
				item.targetx += Math.random() * 40;
			else if (item.targetx >= canvas.width - 80 - item.y)
				item.targetx += Math.random() * 40 - 42;
			else
				item.targetx += Math.random() * 40 - 20;
			if (item.targety <= 20)
				item.targety += Math.random() * 40;
			else if (item.targety >= 500)
				item.targety += Math.random() * 40 - 42;
			else
				item.targety += Math.random() * 40 - 20;
		}

		//Set Velocity to reach Target
		item.velocityX = clamp(item.velocityX + (item.targetx - item.x) / 2000.0, -topSpeed, topSpeed);
		item.velocityY = clamp(item.velocityY + (item.targety - item.y) / 2000.0, -topSpeed, topSpeed);

		//Avoid Mouse Position
		let toMouseDis = getDistance(item.x, item.y, pos.x, pos.y);
		if (toMouseDis < 100 && toMouseDis > 0)
		{
			let vX = (((item.x - pos.x) * (1 / toMouseDis)));
			let vY = (((item.y - pos.y) * (1 / toMouseDis)));
			let fac = 4 - map(toMouseDis, 0, 100, 0, 4);
			item.velocityX += vX * fac;
			item.velocityY += vY * fac;
		}

		//Avoid other points
		for (let innerItem of points)
		{
			let toPointDis = getDistance(item.x, item.y, innerItem.x, innerItem.y);
			if (toPointDis < 50 && toPointDis > 0)
			{
				let veX = (((item.x - innerItem.x) * (1 / toPointDis)));
				let veY = (((item.y - innerItem.y) * (1 / toPointDis)));
				let fact = 0.2 - map(toPointDis, 0, 50, 0, 0.2);
				item.velocityX += veX * fact;
				item.velocityY += veY * fact;
			}
		}

		//Move the points
		item.x += item.velocityX;
		item.y += item.velocityY;

		item.cooldown--;
	}
}

function unfoldContent(obj, at, fullHeight)
{
	if (at >= 100)
	{
		if (!focused)
		{
			obj.style.visibility = "hidden";
			obj.style.gridTemplateRows = "0%";
		}
		return;
	}

	if (focused)
		val = Math.sin((at / 200.0) * Math.PI) * Math.sin((at / 200.0) * Math.PI) * 100;
	else
		val = Math.sin(((at + 100) / 200.0) * Math.PI) * Math.sin(((at + 100) / 200.0) * Math.PI) * 100;

	TBG.style.height = (val / 100.0) * fullHeight + "px";

	onScroll();

	setTimeout(function ()
	{
		unfoldContent(obj, at + 1, fullHeight);
	}, 1);
}


/*
*
*	EventListeners
*
*/
function onScroll()
{
	progressBar.style.transform = `scale(1,${window.pageYOffset / (document.body.scrollHeight - window.innerHeight)})`;
}

function onScrollBarClick(event)
{
	let scrlTo = ((event.pageY - window.pageYOffset) / progressBarContainer.offsetHeight) * (document.body.scrollHeight - progressBarContainer.offsetHeight);

	window.scroll({
		top: scrlTo,
		left: 0,
		behavior: "smooth"
	});
}
function onScrollBarMouseDown(event)
{
	barClicked = true;
}
function onScrollBarMouseUp(event)
{
	barClicked = false;
}

function onMouseMove(event)
{
	event = event || window.event;

	mousePos =
	{
		x: event.pageX,
		y: event.pageY - window.pageYOffset
	};

	if (barClicked)
		window.scrollTo(0, ((event.pageY - window.pageYOffset) / progressBarContainer.offsetHeight) * (document.body.scrollHeight - progressBarContainer.offsetHeight));
}


/*
*
*	Util
*
*/

//Remaps a value from a given Field to a new Field
function map(val, srcFloor, srcCeil, destFloor, destCeil)
{
	return destFloor + ((destCeil - destFloor) * ((val - srcFloor) / (srcCeil - srcFloor)));
}

//Limits a value to the floor minimum and the ceil maximum
function clamp(val, floor, ceil)
{
	if (val < floor)
		return floor;
	else if (val > ceil)
		return ceil;
	else
		return val;
}

///Rescale Canvas to the destined width and heigt with a offset
function rescale(canv, wid, hei, o_wid, o_hei)
{
	if (canv.width != wid + offsetWidth)
	{
		canv.width = wid + o_wid;
		canv.height = hei + o_hei;
	}
}

//Create a HTML Hex Color from rgb values
function rgb(r, g, b)
{
	return "#" + clamp(r, 0, 255).toString(16).padStart(2, '0') + clamp(g, 0, 255).toString(16).padStart(2, '0') + clamp(b, 0, 255).toString(16).padStart(2, '0');
}

//Create a HTML Hex Color from rgba values
function rgba(r, g, b, a)
{
	return rgb(r, g, b) + clamp(a, 0, 255).toString(16).padStart(2, '0');
}

//Calculate the Distance between two 2D-Points
function getDistance(x1, y1, x2, y2)
{
	return Math.sqrt(((x1 - x2) * (x1 - x2))
		+ ((y1 - y2) * (y1 - y2)));
}