def player_data_scrap():
        endpoint_team_names = {
            "1K FC": "1k",
            "Aniquiladores FC": "aniquiladores-fc",
            "El Barrio": "el-barrio",
            "Jijantes FC": "jijantes-fc",
            "Kunisports": "kunisports",
            "Los Troncos FC": "los-troncos-fc",
            "PIO FC": "pio-fc",
            "Porcinos FC": "porcinos-fc",
            "Rayo de Barcelona": "rayo-barcelona",
            "Saiyans FC": "saiyans-fc",
            "Ultimate Móstoles": "ultimate-mostoles",
            "xBuyer Team": "xbuyer-team",
        }
        
        players_data = []
        
        print(endpoint_team_names.items())
        
        for team_name, endpoint in endpoint_team_names.items():
            print("hola")
            
            
            
player_data_scrap()