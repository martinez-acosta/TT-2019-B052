<template>
  <div class="container">
    <div class="row col">
      <v-toolbar dense>
        <v-btn icon>
          <v-icon>mdi-download</v-icon>
        </v-btn>
        <v-btn icon>
          <v-icon>mdi-content-paste</v-icon>
        </v-btn>
        <v-spacer></v-spacer>
        <v-btn icon>
          <v-icon>mdi-help</v-icon>
        </v-btn>
      </v-toolbar>
    </div>
    <div class="comtaier overflow-auto">
      <ssh-pre language="sql" label="SQL">{{ sentences }}</ssh-pre>
    </div>
  </div>
</template>

<script type="module">
import SshPre from 'simple-syntax-highlighter'
import 'simple-syntax-highlighter/dist/sshpre.css'

export default {
  components: { SshPre },
  data() {
    return {
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
