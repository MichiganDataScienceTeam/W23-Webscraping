library(shiny)
library(readr)
library(ggplot2)
library(dplyr)
library(DT)
library(shinyjs)

df <- read_csv('data/cse_final.csv', show_col_types=FALSE)
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
        value = c(min(df$clarity, na.rm=TRUE), max(df$clarity, na.rm=TRUE)),
        min = 0, 
        max = 100
        ),
      
      sliderInput(
        "preparedness_range", "Preparedness", 
        value = c(min(df$preparedness, na.rm=TRUE), max(df$preparedness, na.rm=TRUE)),
        min = 0, 
        max = 100
        ),
      
      sliderInput(
        "respect_range", "Respect", 
        value = c(min(df$respect, na.rm=TRUE), max(df$respect, na.rm=TRUE)),
        min = 0, 
        max = 100
        ),
      
      checkboxInput("research_check", "Has an Open Research Position?"),
      checkboxInput("taught_check", "Has The Professor Taught/Been Evaluated?")
      
    ),
    
    
    dataTableOutput("profs")
    
  )
)

server <- function(input, output) {
  # Filter data based on range sliders
  filtered_data <- reactive({

    if (input$taught_check) {
      df %>% 
      filter( 
        input$clarity_range[1]<= clarity & clarity <= input$clarity_range[2] &
        input$preparedness_range[1] <= preparedness & preparedness <= input$preparedness_range[2] &
        input$respect_range[1] <= respect & respect <= input$respect_range[2] &
        (!input$research_check | research)
      )
    }
    else {
      df
    }
         
  })
  
  # Display filtered data in table format
  output$profs <- renderDataTable({
    filtered_data() %>% 
      select(name, email, clarity, preparedness, respect, research, lab, interests)
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
        renderText(paste0("Students Taught: ", row_data$`students taught`)),
        renderText(paste0("Terms Taught: ", row_data$`terms taught`)),
        easyClose = TRUE, footer = NULL
      ))
    }
  })
}


# Run the application 
shinyApp(ui = ui, server = server)