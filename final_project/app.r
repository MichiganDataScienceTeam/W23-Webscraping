library(shiny)
library(tidyverse)
library(ggplot2)
library(dplyr)
library(DT)

df <- read_csv('data/dummy_ai.csv')
#print(df)



# Define UI for application that draws a histogram
ui <- fluidPage(
  
  # Application title
  titlePanel("UM Professors"),
  
  sidebarLayout(
    sidebarPanel(
      ## add four inputs for the minimum and maximum x and y values
      ## make sure to use checking so that users can't exceed these values
      sliderInput(
        "clarity_range", "Clarity", 
        value = c(min(df$clarity), max(df$clarity)),
        min = min(df$clarity), 
        max = max(df$clarity)
        ),
      
      sliderInput(
        "preparedness_range", "Preparedness", 
        value = c(min(df$preparedness), max(df$preparedness)),
        min = min(df$preparedness), 
        max = max(df$preparedness)
        ),
      
      sliderInput(
        "respect_range", "Respect", 
        value = c(min(df$respect), max(df$respect)),
        min = min(df$respect), 
        max = max(df$respect)
        ),
      
      checkboxInput("research_check", "Has an Open Research Position?")
      
    ),
    
    
    dataTableOutput("profs")
    
  )
)

server <- function(input, output) {
  # Filter data based on range sliders
  filtered_data <- reactive({
    df %>% 
      filter( 
        input$clarity_range[1]<= clarity & clarity <= input$clarity_range[2] &
        input$preparedness_range[1] <= preparedness & preparedness <= input$preparedness_range[2] &
        input$respect_range[1] <= respect & respect <= input$respect_range[2] &
        (!input$research_check | research)
      )
           
  })
  
  # Display filtered data in table format
  output$profs <- renderDataTable({
    filtered_data()
  }, options= list(pageLength=5))
}

# Run the application 
shinyApp(ui = ui, server = server)