<template>
  <div class="container">
    <div class="row col">
      <v-toolbar dense>
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-btn icon v-bind="attrs" v-on="on">
              <v-icon>mdi-download</v-icon>
            </v-btn>
          </template>
          <span>Descargar</span>
        </v-tooltip>

        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-btn icon v-bind="attrs" v-on="on">
              <v-icon>mdi-content-paste</v-icon>
            </v-btn>
          </template>
          <span>Copiar al portapapeles</span>
        </v-tooltip>

        <v-spacer></v-spacer>

        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              icon
              v-bind="attrs"
              v-on="on"
              @click.stop="helpDialog = true"
            >
              <v-icon>mdi-help</v-icon>
            </v-btn>
          </template>
          <span>Ayuda</span>
        </v-tooltip>
      </v-toolbar>
    </div>

    <div class="comtaier overflow-auto">
      <ssh-pre language="sql" label="SQL">{{ sentences }}</ssh-pre>
    </div>

    <!-- Dialog/modals -->
    <v-dialog v-model="helpDialog" max-width="360">
      <v-card>
        <v-card-title class="headline"
          >Sentencias SQL equivalentes al diagrama ER</v-card-title
        >

        <v-card-text>
          En este apartado puede observar las sentencias SQL equivalentes al
          diagrama entidad-relación generado en el paso 1. <br />
          Puede copiar o descargar estas sencentencias para comprobar su
          correcto funcionamiento en el gestor de base de datos MySQL.
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" text @click="helpDialog = false"
            >De acuerdo</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script type="module">
import SshPre from 'simple-syntax-highlighter'
import 'simple-syntax-highlighter/dist/sshpre.css'

export default {
  components: { SshPre },
  data() {
    return {
      helpDialog: false,
      sentences: `/*
*********************************************************************
Name: MySQL Sample Database classicmodels
Version 3.1
+ changed data type from DOUBLE to DECIMAL for amount columns
Version 3.0
+ changed DATETIME to DATE for some colunmns
Version 2.0
+ changed table type from MyISAM to InnoDB
+ added foreign keys for all tables 
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

CREATE DATABASE IF NOT EXISTS 'classicmodels';

USE 'classicmodels';

/*Table structure for table 'customers' */

DROP TABLE IF EXISTS 'customers';

CREATE TABLE 'customers' (
  'customerNumber' int(11) NOT NULL,
  'customerName' varchar(50) NOT NULL,
  'contactLastName' varchar(50) NOT NULL,
  'contactFirstName' varchar(50) NOT NULL,
  'phone' varchar(50) NOT NULL,
  'addressLine1' varchar(50) NOT NULL,
  'addressLine2' varchar(50) DEFAULT NULL,
  'city' varchar(50) NOT NULL,
  'state' varchar(50) DEFAULT NULL,
  'postalCode' varchar(15) DEFAULT NULL,
  'country' varchar(50) NOT NULL,
  'salesRepEmployeeNumber' int(11) DEFAULT NULL,
  'creditLimit' decimal(10,2) DEFAULT NULL,
  PRIMARY KEY ('customerNumber'),
  KEY 'salesRepEmployeeNumber' ('salesRepEmployeeNumber'),
  CONSTRAINT 'customers_ibfk_1' FOREIGN KEY ('salesRepEmployeeNumber') REFERENCES 'employees' ('employeeNumber')
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
`
    }
  }
}
</script>