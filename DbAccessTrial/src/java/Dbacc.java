import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;
import java.sql.*;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.json.*;
 
public class Dbacc extends HttpServlet{

   @Override
   public void doPost(HttpServletRequest request, HttpServletResponse response)
      throws ServletException, IOException {
       PrintWriter out=response.getWriter();
       response.setContentType("text/html");
     
    try {
         //Class.forName("com.mysql.jdbc.Driver");
         String jdbcUrl="jdbc:mysql://localhost:3306/customerreviews";
         String username="root";
         String password="pradeepika";
         Connection conn = null;
           try {
               DriverManager.registerDriver(new com.mysql.jdbc.Driver());
               conn = DriverManager.getConnection(jdbcUrl, username, password);
           } catch (SQLException ex) {
               Logger.getLogger(Dbacc.class.getName()).log(Level.SEVERE, null, ex);
           }
         Statement stmt = conn.createStatement();
         String sql = "SELECT sno, sentiment, author, comment, website_name, loc  FROM product_reviews";
         ResultSet rs = stmt.executeQuery(sql);
         
           try {
               JSONArray arr=new JSONArray();
                              JSONObject finalObj=new JSONObject();

               while(rs.next()){
                   int sno  = rs.getInt("sno");
                   String sentiment = rs.getString("sentiment");
                   String name = rs.getString("author");
                   String content = rs.getString("comment");
                   String website = rs.getString("website_name");
                   String location = rs.getString("loc");
                   //out.println(sentiment);
                   JSONObject obj = new JSONObject(sentiment);
                   double compound=obj.getDouble("compound");
                   JSONObject obj1 = new JSONObject();
                   obj1.put("compound", compound);
                   obj1.put("name", name);
                   obj1.put("loc", location);
                   //out.println(obj1.toString());
                   if(finalObj.has(website)){
                       finalObj.getJSONArray(website).put(obj1);
                   }else{
                       finalObj.put(website, new JSONArray());
                       finalObj.getJSONArray(website).put(obj1);
                   }
                   //arr.put(obj1);
                   
                   
               }out.println(finalObj.toString());
            } catch (SQLException ex) {
               Logger.getLogger(Dbacc.class.getName()).log(Level.SEVERE, null, ex);
           }
         conn.close();
    }
        
/*catch(ClassNotFoundException e) {
         e.printStackTrace(); 
}*/      catch (SQLException ex) {
           Logger.getLogger(Dbacc.class.getName()).log(Level.SEVERE, null, ex);
       }
}
/*catch(SQLException se) {
         se.printStackTrace();
      } */
}