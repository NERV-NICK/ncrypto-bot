let tg = window.Telegram.WebApp
tg.headerColor = '#000000'
tg.expand()

let url = 'https://ncrypto-bot.onrender.com'

async function fetchData(action, data) {
	try {
		let response = await axios.post(`${url}/${action}`, data)
		return response.data
	} catch (error) {
		console.log(error)
	}
}

var score = parseInt(document.getElementById('score').innerHTML)
var prevScore = score

function formatScore(score) {
	const units = ['K', 'M', 'B', 'T']
	const unit = Math.floor((score.toString().length - 1) / 3)
	const formattedScore = (score / Math.pow(1000, unit)).toFixed(1)
	return formattedScore.replace('.0', '') + (units[unit - 1] || '')
}

document.querySelector('#ncoin').addEventListener('click', async () => {
	var number = document.createElement('div')
	number.textContent = '+1'
	number.className = 'tap'
	number.style.fontSize = '50px'
	number.style.left = event.clientX + 'px'
	number.style.top = event.clientY + 'px'
	document.body.appendChild(number)
	score += 1
	document.getElementById('score').innerHTML = formatScore(score)
	number.addEventListener('animationend', function () {
		document.body.removeChild(number)
	})
})

setInterval(async function () {
	if (score !== prevScore) {
		await fetchData('score', {
			id: tg.initDataUnsafe.user.id,
			score: score,
		})
	}
	prevScore = score
}, 10000)

document.addEventListener('DOMContentLoaded', event => {
	document.getElementById('score').innerHTML = formatScore(score)
})

function copyLink() {
	var copyText = document.getElementById('linkField')
	copyText.select()
	copyText.setSelectionRange(0, 99999)
	navigator.clipboard.writeText(copyText.value)
	alert('Ссылка скопирована: ' + copyText.value)
}
