/// <reference types="cypress" />
let filepath = "PenguinBra.jpg"

context('Actions', () => {
  beforeEach(() => {
    cy.visit('https://tdt4242-axell-vegard-frontend.herokuapp.com/')
    cy.contains("Log in").click()

    cy.get("form").children().first().type("admin")
        .next().type("12345")
        .next().click()
        .next().click()
  })

  it('Log new workout', () =>{
    cy.get("#btn-create-workout").click()

    cy.wait(3000)
    cy.get("form").children().first().type("abc")
        .next().next().type("2017-06-01T08:30")
        .next().next().next().type("Public")
        .next().type("I did a nice workout without much result butt alot of glamor for my bois")
        .next().next().get('[id="customFile"]')
        .attachFile(filepath)

    cy.get('#btn-ok-workout').click()
  })

  it('Log new workout', () =>{
    cy.get("#btn-create-workout").click()

    cy.wait(3000)
    cy.get("form").children().first().type("title")
        .next().next().type("2017-06-01T08:30")
        .next().next().next().type("Public")
        .next().type("I did a nice workout without much result butt alot of glamor for my bois")
        .next().next().get('[id="customFile"]')
        .attachFile(filepath)

    cy.get('#btn-ok-workout').click()

    cy.get('#inpt-search-keyword').type("title")
    cy.get('#btn-search-button').click()
  })

})