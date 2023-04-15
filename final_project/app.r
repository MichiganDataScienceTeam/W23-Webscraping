library(shiny)
library(readr)
library(ggplot2)
library(dplyr)
library(DT)
library(shinyjs)

df <- read_csv('data/dummy_cse.csv', show_col_types=FALSE)
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
    filtered_data() %>% 
      select(name, email, clarity, preparedness, respect, research, interests)
  }, options = list(pageLength = 5), server = TRUE)

  # Display selected row data in popup when a row is clicked
  observeEvent(input$profs_rows_selected, {
    if(length(input$profs_rows_selected) == 1){
      row_data <- filtered_data() %>% slice(input$profs_rows_selected)
      showModal(modalDialog(
        renderText(paste0("Name: ", row_data$name)),
        renderText(paste0("Email: ", row_data$email)),
        renderText(paste0("Lab: ", row_data$lab)),
        renderText(paste0("Office: ", row_data$office)),
        renderText(paste0("Clarity: ", row_data$clarity)),
        renderText(paste0("Preparedness: ", row_data$preparedness)),
        renderText(paste0("Respect: ", row_data$respect)),
        renderText(paste0("Research: ", row_data$research)),
        renderText(paste0("Interests: ", row_data$interests)),
        easyClose = TRUE, footer = NULL
      ))
    }
  })
}


# Run the application 
shinyApp(ui = ui, server = server)