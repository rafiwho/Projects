class BOOKS{
    String name,author;
    int edition;
    BOOKS(String name,String author,int edition){
        this.name = name;
        this.author = author;
        this.edition = edition;
    }
    String getName(){
        return name;
    }
    String getAuthor(){
        return author;
    }
    int getEdition(){
        return edition;
    }
    void setName(String name){
       this.name = name;
    }
    void setAuthor(String author){
        this.author = author;
    }
    void setEdition(int edition){
        this.edition = edition;
    }
    
}
class HelloWorld {
    public static void main(String[] args) {
        System.out.println("*******Digital Libray of DIU: Book List**********\n");
       BOOKS book1 = new BOOKS("Introduction to Computer Fundamental","PK SINHA",5);
       BOOKS book2 = new BOOKS("Introduction to Algorithms","THOMAS H.",6);
       System.out.println("Book1: "+book1.getName()+",Author: "+book1.getAuthor()+",Edition: "+book1.getEdition()+"th");
        System.out.println("Book2: "+book2.getName()+",Author: "+book2.getAuthor()+",Edition: "+book2.getEdition()+"th");
       
       book1.setEdition(6);
       book2.setAuthor("Thomas H. Cormen");
       book2.setEdition(6);
       
       System.out.println("\nInformation Updated");
       System.out.println("UPDATED INFORMATITION:\n");
        System.out.println("Book1: "+book1.getName()+",Author: "+book1.getAuthor()+",Edition: "+book1.getEdition()+"th");
        System.out.println("Book2: "+book2.getName()+",Author: "+book2.getAuthor()+",Edition: "+book2.getEdition()+"th");
     
    }
}
