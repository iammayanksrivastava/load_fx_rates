        ## This part of the code writes the data to a csv file. 
        file = None
        
        try: 
            with(open(f'../data/historical_rates_{base}_{date}_{formatted_time}.csv', 'w', newline='')) as file:
                file.write(output.getvalue())
                logger.info(f'File extracted with historical rates of {date} and {base}')
        
        except Exception as e: 
            logger.error(f"An error occurred: {e}", exc_info=True)
            return False
        finally: 
            output.close()