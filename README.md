# CROSS GUILD LEAGUE BOT

This monorepo contains services to run the Cross Guild One Piece TCG League at Atomic Empire through Discord.

## Services

- Discord service (/discord)
    - The discord bot integration that sends achievement lists and listens to reactions
- API (/api)
    - The web backend that handles the data access layer for other services
- Postgres (/postgres)
    - Persistent database storage
- Frontend (/frontend)
    - App for viewing the leaderboard and current achievements

## Dev Setup
All services are containerized. Reach out to @hardingalexh for a .env file to include at root with all necessary credentials, then run `docker compose up`.