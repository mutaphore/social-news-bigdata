import java.util.*;
import java.io.IOException;

import java.sql.Timestamp;
import java.util.Date;


public class Test {


        public static void main(String [] args) {
            java.util.Date date= new java.util.Date(Integer.parseInt(args[0]) * 1000);
            System.out.println(date.getHours());
        }


}
