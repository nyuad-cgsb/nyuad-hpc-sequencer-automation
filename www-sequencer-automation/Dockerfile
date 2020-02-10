FROM node:9

RUN npm install -g @angular/cli@6.2.2
ENV NODE_ENV=dev

RUN mkdir -p /home/node/www-sequencer-automation && chown -R node:node /home/node/www-sequencer-automation
RUN mkdir -p /home/node/www-sequencer-automation/node_modules && chown -R node:node /home/node/www-sequencer-automation/node_modules

WORKDIR /home/node/www-sequencer-automation

#CMD npm install && \
#  bash -c "ng build; ng serve --host=0.0.0.0 --port 4200"
CMD npm install && \
  bash -c "tail -f /dev/null"
