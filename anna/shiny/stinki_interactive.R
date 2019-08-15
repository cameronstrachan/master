library(shiny)
library(ggplot2)
library(Cairo)   # For nicer ggplot2 output when deployed on Linux

ui <- fluidPage(
  fluidRow(
    column(width = 12,
           plotOutput("plot1", height = 250,hover = hoverOpts(id ="plot_hover"))
    )
  ),
  fluidRow(
    column(width = 5,
           verbatimTextOutput("hover_info")
    )
  )
)

server <- function(input, output) {
  
  
  output$plot1 <- renderPlot({
    
    plot_stinki
    
  })
  
  output$hover_info <- renderPrint({
    if(!is.null(input$plot_hover)){
      hover=input$plot_hover
      dist=sqrt((hover$x-df_plot_noah$gene1)^2+(hover$y-df_plot_noah$mean_pi)^2)
      cat("Gene ID\n")
      if(min(dist) < 6)
        df_plot_noah$qseqid[which.min(dist)]
    }
    
    
  })
}

shinyApp(ui, server)