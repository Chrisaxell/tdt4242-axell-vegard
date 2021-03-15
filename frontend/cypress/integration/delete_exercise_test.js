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

  it('Delete Exercise', () =>{
    cy.get("#btn-create-workout").click()

    cy.wait(3000)
    cy.get('#btn-add-exercise').click()
    cy.wait(2000)
    cy.get(".delete-exercise-button").click({multiple: true})
    /*cy.wait(1000)
    cy.get('#div-exercises').should('be.empty')*/

  })
})