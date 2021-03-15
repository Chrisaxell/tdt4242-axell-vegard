/// <reference types="cypress" />

context('Actions', () => {
  beforeEach(() => {
    cy.visit('https://tdt4242-axell-vegard-frontend.herokuapp.com/')
  })

  it('Make new excercise', () =>{
    cy.get("#btn-login-nav").click()
    cy.get("form").children().first().type("admin")
        .next().type("12345")
        .next().click()
        .next().click()
    cy.wait(2000)
    cy.get('#nav-exercises').click({force: true})
    cy.get("#btn-create-exercise").click()
    cy.get("form").children().first().type("Leg Squat")
        .next().next().type("You stand on one leg and do a squat with the other legg resting in the air")
        .next().next().type("nr")
    cy.get("#btn-ok-exercise").click()
    cy.wait(2000)
  })

  it('Try to delete excecise', () =>{
    cy.get("#btn-login-nav").click()
    cy.get("form").children().first().type("admin2")
        .next().type("12345")
        .next().click()
        .next().click()
    cy.wait(2000)
    cy.get('#nav-exercises').click({force: true})
    cy.get("#div-content").first().click()
    cy.get("btn-edit-exercise").should('not.exist')
  })
})