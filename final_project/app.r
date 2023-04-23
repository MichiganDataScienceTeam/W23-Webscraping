library(shiny)
library(readr)
library(ggplot2)
library(dplyr)
library(DT)
library(shinyjs)

df <- read_csv('data/cse_final.csv', show_col_types=FALSE)
# Convert "lab" and "interests" columns to vectors
df$lab <- gsub("\\[|\\]|\\'", "", df$lab)  # remove square brackets
df$lab <- strsplit(df$lab, ",\\s*")    # split by comma and whitespace

df$interests <- gsub("\\[|\\]|\\'", "", df$interests)
df$interests <- strsplit(df$interests, ",\\s*")
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

      renderText("Labs Professor Works in"),
      checkboxInput("ai_check", "AI", value=TRUE),
      checkboxInput("theory_check", "Theory", value=TRUE),
      checkboxInput("ce_check", "CE", value=TRUE),
      checkboxInput("systems_check", "Systems", value=TRUE),
      checkboxInput("cse_teaching_check", "CSE-Teaching", value=TRUE),
      checkboxInput("hcc_check", "HCC", value=TRUE),

      checkboxInput("taught_check", "Has The Professor Taught/Been Evaluated?")
    ),
    
    
    dataTableOutput("profs")
    
  )
)

filter_lab <- function(df, input) {
  include <- list(
    c('ai', input$ai_check),
    c('theory', input$theory_check),
    c('ce', input$ce_check),
    c('systems', input$systems_check),
    c('cse-teaching', input$cse_teaching_check),
    c('hcc', input$hcc_check)
  ) 
  
  filtered_include <- Filter(function(x) x[2], include)
  filtered_include <- unlist(lapply(filtered_include, function(x) x[1]))

  df[sapply(df$lab, function(x) any(x %in% filtered_include)), ]
}




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
      ) %>%
      filter_lab(input)
    }
    else {
      df %>% filter(
        (!input$research_check | research)
      ) %>% filter_lab(input)
    }
         
  })
  
  # Display filtered data in table format
  output$profs <- renderDataTable({
    filtered_data() %>% 
      select(name, email, clarity, preparedness, respect, research, lab, interests) %>%
      datatable(
        options = list(
          pageLength = 5,
          columnDefs = list(list(targets = c(6,7,8), orderable = FALSE))
        )
      )
  }, server = TRUE)


  # Display selected row data in popup when a row is clicked
  observeEvent(input$profs_rows_selected, {
    if(length(input$profs_rows_selected) == 1){
      row_data <- filtered_data() %>% slice(input$profs_rows_selected)
      showModal(modalDialog(
        renderText(paste0("Name: ", row_data$name)),
        renderText(paste0("Email: ", row_data$email)),
        renderText(paste0("Lab: ", row_data$lab)),
        renderText(paste0("Office: ", row_data$office)),
        if(!is.na(row_data$website)) renderText(paste0("Website: ", row_data$website)),
        if(!is.na(row_data$phone)) renderText(paste0("Phone: ", row_data$phone)),
        renderText(paste0("Students Taught: ", row_data$`students taught`)),
        renderText(paste0("Terms Taught: ", row_data$`terms taught`)),
        easyClose = TRUE, footer = NULL
      ))
    }
  })
}


# Run the application 
shinyApp(ui = ui, server = server)