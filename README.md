# PirateBot

This project is a discord bot that allows you to play the Pirate Game

To add the bot to your server without hosting it yourself, you can invite the bot [here](https://discord.com/api/oauth2/authorize?client_id=938879385870676008&permissions=149251632208&scope=bot)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

To run this project localy you will need 
* Python (3.9 or higher)
* python discord module

Python can be downloaded from [python.org](https://www.python.org/downloads/).

The python discord module can be installed using the following command:
```
pip install discord
```

### Installing

To download the files required download teh lastest version of the repo or use the following command
```
git clone https://github.com/jdf18/PirateBot.git
```

## Deployment

To deploy your own version of this project, you need to [create a discord bot application](https://discord.com/developers/applications/).

You can then add this bot to your server by going to OAuth2 and then URL Generator.

In the source directory, create a file called .env and copy in the token for your discord bot.

You can then run the python file with
```
python3 main.py
```

## Usage

### Commands
* !pirate start - Begins the pirate game in your current voice channel (WIP)



## Built With

* [Python](https://www.python.org) - The programming language used 
* [GitHub](https://github.com) - The SCM Software Used

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Jacob Flint** - *something1* - [jdf18](https://github.com/jdf18)
* **James Walker** - *something2* - 

See also the list of [contributors](https://github.com/jdf18/PirateBot/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* Great api reference for the [python discord module](https://discordpy.readthedocs.io/en/stable/api.html)
* Charlie Yuen for making us do it

