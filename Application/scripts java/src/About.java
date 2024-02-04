import java.awt.Color;
import java.awt.EventQueue;
import java.awt.Font;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.event.MouseMotionAdapter;
import java.awt.geom.RoundRectangle2D;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

import javax.swing.BorderFactory;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.UIManager;
import javax.swing.UnsupportedLookAndFeelException;

import com.formdev.flatlaf.FlatDarculaLaf;
import java.awt.Toolkit;


////////////////////////////////////////////////////////////////////////////////-----------Fenetre Menu Medecin------------///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

public class About extends JFrame {
	

	private static final long serialVersionUID = 1L;

	//protected static final String ID_Med = null;
	
	Connection cnx=null;
	PreparedStatement prepared = null;
	ResultSet resultat =null; 
	
	private int posX = 0;   //Position X de la souris au clic
    private int posY = 0;   //Position Y de la souris au clic
    

	private JPanel contentPane;
	
	private JTextArea testAreaDesc;
	private JScrollPane scrollpane; 

	/**
	 * Launch the application.
	 * @throws UnsupportedLookAndFeelException 
	 */
	public static void main(String[] args) throws UnsupportedLookAndFeelException {
		FlatDarculaLaf.install();	
		UIManager.setLookAndFeel(new FlatDarculaLaf() );
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					About frame = new About("-1","NONE",false);
					frame.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}
	

	/**
	 * Create the frame.
	 */
	public About(String dataset,String path_data,Boolean DataProcessed ) {
		setIconImage(Toolkit.getDefaultToolkit().getImage(About.class.getResource("/Menu_img/about.png")));
		//cnx

		setUndecorated(true);	
		setResizable(false);

		setTitle("About ?");
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(0, 0, 1100, 650);
		setShape(new RoundRectangle2D.Double(0d, 0d, 1100d, 650d, 25d, 25d));
		setLocationRelativeTo(null);
		//vu que la frame est Undecorated on a besoin de ces MouseListeners pour la faire bouger(frame)
		  addMouseListener(new MouseAdapter() {
	            @Override
	            //on recupere les coordonnées de la souris
	            public void mousePressed(MouseEvent e) {
	                posX = e.getX();    //Position X de la souris au clic
	                posY = e.getY();    //Position Y de la souris au clic
	            }
	        });
	        addMouseMotionListener(new MouseMotionAdapter() {
	            // A chaque deplacement on recalcul le positionnement de la fenetre
	            @Override
	            public void mouseDragged(MouseEvent e) {
	                int depX = e.getX() - posX;
	                int depY = e.getY() - posY;
	                setLocation(getX()+depX, getY()+depY);
	            }
	        });
	        
	        
		contentPane = new JPanel();
		setContentPane(contentPane);
		contentPane.setLayout(null);
		
		JLabel BGModels = new JLabel("");
		BGModels.setIcon(new ImageIcon(About.class.getResource("/About_img/About.png")));
		//BGModels.setIcon(new ImageIcon(Models.class.getResource("/Menu_img/1.png")));	// Back ground de base	
       
// Bouton Reduire ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		JButton Minimise_BTN = new JButton("");
		Minimise_BTN.addMouseListener(new MouseAdapter() {
			@Override
			public void mouseEntered(MouseEvent e) {
				Minimise_BTN.setIcon(new ImageIcon(About.class.getResource("/Menu_img/Minimize ML selected.png")));
			}
			@Override
			public void mouseExited(MouseEvent e) {
				Minimise_BTN.setIcon(new ImageIcon(About.class.getResource("/Menu_img/Minimize ML .png")));
			}
		});
		Minimise_BTN.setToolTipText("Minimize");
		ButtonStyle(Minimise_BTN);
		Minimise_BTN.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				setState(ICONIFIED);
				
			}
		});
		Minimise_BTN.setIcon(new ImageIcon(About.class.getResource("/Menu_img/Minimize ML .png")));
		Minimise_BTN.setBounds(932, 11, 32, 32);
		contentPane.add(Minimise_BTN);
//Boutton home//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
				JButton btnHome = new JButton("");
				btnHome.addMouseListener(new MouseAdapter() {
					@Override
					public void mouseEntered(MouseEvent e) {
						if (btnHome.isEnabled()) {
							btnHome.setIcon(new ImageIcon(About.class.getResource("/Models_img/home selected.png")));//changer les couleurs button
						}
					}
					@Override
					public void mouseExited(MouseEvent e) {
						if (btnHome.isEnabled()) {
							btnHome.setIcon(new ImageIcon(About.class.getResource("/Models_img/home.png")));//remetre le bouton de base
						}
					}
				});
				btnHome.addActionListener(new ActionListener() {
					public void actionPerformed(ActionEvent e) {
							Menu frame = new Menu(dataset,path_data,DataProcessed);// retourner au menu medecin
							frame.setLocationRelativeTo(null);
							frame.setVisible(true);
							dispose();
					}
				});
				btnHome.setIcon(new ImageIcon(About.class.getResource("/Models_img/home.png")));
				btnHome.setToolTipText("Menu");
				btnHome.setBounds(974, 11, 32, 32);
				ButtonStyle(btnHome);
				contentPane.add(btnHome);
// Exit bouton//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		
		JButton Exit_BTN = new JButton("");
		Exit_BTN.addMouseListener(new MouseAdapter() {
			@Override
			public void mouseEntered(MouseEvent arg0) {
				Exit_BTN.setIcon(new ImageIcon(About.class.getResource("/Menu_img/Exit ML selected.png")));
			}
			@Override
			public void mouseExited(MouseEvent arg0) {
				Exit_BTN.setIcon(new ImageIcon(About.class.getResource("/Menu_img/Exit ML.png")));
			}
		});
		Exit_BTN.setToolTipText("Exit");
		ButtonStyle(Exit_BTN);
		Exit_BTN.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
			
					
					int ClickedButton	=JOptionPane.showConfirmDialog(null, "Do you really want to leave?", "Close", JOptionPane.YES_NO_OPTION);
					if(ClickedButton==JOptionPane.YES_OPTION)
					{					
						dispose();
					}
					
					
			}
			
		});
		Exit_BTN.setIcon(new ImageIcon(About.class.getResource("/Menu_img/Exit ML.png")));
		Exit_BTN.setBounds(1016, 11, 32, 32);
		contentPane.add(Exit_BTN);
	

		
		scrollpane = new JScrollPane();
		scrollpane.setBounds(107, 165, 869, 290);
		scrollpane.setBorder(BorderFactory.createEmptyBorder());
		scrollpane.getViewport().setOpaque(false);
		contentPane.add(scrollpane);
		
		testAreaDesc = new JTextArea();
		scrollpane.setViewportView(testAreaDesc);
		testAreaDesc.setBackground(new Color(255, 51, 51));
		testAreaDesc.setForeground(Color.WHITE);
		testAreaDesc.setFont(new Font("Microsoft PhagsPa", Font.BOLD, 16));
		testAreaDesc.setText("Nous nous intéressons à la proposition d’une solution de recommandation dans un contexte social. \n"
				+ "La dimension sociale est caractérisée par les liens d’amitié, de confiance et d’influence entre les membres du réseau. \r\n" + 
				"Les systèmes de recommandations visent à proposer aux utilisateurs des items en lien avec leur consultation en cours et qui\n"
				+ " peuvent retenir leur intérêt. L’intérêt des utilisateurs dépend du contexte dans lequel ils se trouvent. \r\n" + 
				"Dans ce travail, il s’agit de proposer un système hybride combinant les algorithmes de filtrage collaboratif (FC) \n"
				+ "et social (Fsoc) d'un côté, et d'un autre côté l'algorithme de recommandation hybride doit être sensible au contexte. \r\n" + 
				"Kulkarni et Rodd (2020) ont publié une revue de la littérature sur les techniques existantes pour la recommandation\n"
				+ " contextuelle qu'ils ont classé en : (1) techniques bio-inspirées (exemple : les réseaux de neurones et les algorithmes \n"
				+ "d'optimisation comme l'algorithme génétique) ; et (2) techniques statistiques (exemple: Matrix factorization - MF; K-plus \n"
				+ "proches voisins - KNN, Support Vector Machine  - SVM, Latent Dirichlet Allocation - LDA...)\r\n" + 
				"Ainsi, le contexte pourrait être défini comme l’objectif ou l’intention de l’utilisateur, modélisé par une approche LDA\n"
				+ " qui génère un modèle de thèmes pour chaque intention. \r\n" + 
				"L'état de l'art présenté dans (Kulkarni et Rodd, 2020)  ne précise pas l'existence de travaux sur la recommandation basés \n"
				+ "sur le contexte en utilisant des techniques de Deep learning (DL). Pour cela, nous sommes motivés dans ce projet à implémenter\n"
				+ " une solution de recommandation contextuelle en considérant une technique de DL. Afin de montrer l'apport de ce choix, les\n"
				+ " étudiants vont également implémenter deux autres techniques bio-inspirée et statistique afin de comparer les résultats.\r\n" + 
				"Un système de recommandation sera implémenté sur la base de cette approche de recommandation contextuelle (qui va inclure \n"
				+ "un ensemble d'algorithmes). Une expérimentation avec évaluation et comparaisons des différents algorithmes sera effectuée en "
				+ "\n"
				+ "utilisant une à deux bases de tests. \r\n" + 
				"");
		testAreaDesc.setRows(10);
		testAreaDesc.setEditable(false);
		testAreaDesc.setSelectionStart(0);// le xceollpane affiche de haut en bas
		testAreaDesc.setSelectionEnd(0);
		testAreaDesc.setOpaque(false);
		testAreaDesc.setColumns(10);
		
//le background////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		BGModels.setBounds(0, 0, 1100, 650);
		contentPane.add(BGModels);
		
	}
//methode du style des buttons/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	 private void ButtonStyle(JButton btn) {
	//enlecer les bordures des btn
	 btn.setOpaque(false);
	 btn.setFocusPainted(false);
	 btn.setBorderPainted(false);
	 btn.setContentAreaFilled(false);
	
}
}
