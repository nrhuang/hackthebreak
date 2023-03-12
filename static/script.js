const jobCardTemplate = document.querySelector("[data-job-template]")
const jobCardContainer = document.querySelector("[data-job-cards-container]")
const searchInput = document.querySelector("[data-search]")

let jobs = []

searchInput.addEventListener("input", e => {
    const value = e.target.value.toLowerCase()
    jobs.forEach(job => {
        const isVisible = job.name.toLowerCase().includes(value) || job.conpany.includes(value)
        job.element.classList.toLowerCase().toggle("hide", !isVisible)
    })
})

fetch('../jobs.json').then(response =>
        response.json())
    .then(json => {
        data.map(job => {
            const card = userCardTemplate.content.cloneNode(true).children[0]
            const header = card.querySelector("[data-header]")
            const body = card.querySelector("[data-body]")
            header.textContent = job.name
            body.textContent = job.company
            body.textContent = job.rating
            userCardContaner.append(card)
            return {name: job.name, company: user.company, element: card}
        })
})
