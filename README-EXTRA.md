# DAPI - Extra
## Your own RPC

1. Open file `settings.json`
2. Find `"richPresenceProfiles"`
3. Add in this dict value:
   ```json lines
   ...
   "test": {
       "clientID": "<your_application_id>",
       "details": "Details",
       "state": "State",
       "startTimestamp": null,
       "endTimestamp": null,
       "largeImage": {
           "imgName": "img1",
           "text": "LargeText"
       },
       "smallImage": {
           "imgName": "img2",
           "text": "SmallText"
       },
       "animation": null,
       "buttons": [
           {
               "label": "Link1",
               "url": "https://github.com/Mon4ik/"
           },
           {
               "label": "Link2",
               "url": "https://github.com/Mon4ik/DAPI"
       ]
   }
   ...
   ```
4. Done

## Your own status animation

1. Open file `settings.json`
2. Find `"statusAnimProfiles"`
3. Add in this dict value:
   ```json lines
   ...
   "profileName": {
       "texts": [
           "Text 1",
           "Text 2",
           "Text 3"
       ],
       "emoji": null
   }
   ...
   ```
4. Done