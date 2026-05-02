# Documentation - Pong!

## Notes

### Moving the pads

- Right now  I need to find a way to create up-down borders for the pads. No part of the pad should be able to escape the screen. 
- I've been able to do that right now but it's not the cleanest. Around the borders it looks laggy. 
    
**What I want:**

- When the pad is between the borders, it can move freely up or down.
- When it tries going **below the bottom border**, it instantly gets brought back to the edge of the border and its ***ability to move downwards is disabled.*** However, it can still move upwards
- Similarly, if it tries going above the top border, it instantly gets brought back to the edge of the top border, and it is ***no longer allowed to move upwards***. But, it can still move down. 

- In order to do this, the abilities to move up and down need to be **callable** - that way, i can only call them when the conditions for them are met.