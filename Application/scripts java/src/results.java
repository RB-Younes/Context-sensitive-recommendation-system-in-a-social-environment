import java.awt.EventQueue;
import java.awt.Toolkit;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.event.MouseMotionAdapter;
import java.awt.geom.RoundRectangle2D;

import javax.swing.BorderFactory;
import javax.swing.ButtonGroup;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JRadioButton;
import javax.swing.JScrollPane;
import javax.swing.UIManager;
import javax.swing.UnsupportedLookAndFeelException;

import com.formdev.flatlaf.FlatDarculaLaf;


////////////////////////////////////////////////////////////////////////////////-----------Fenetre  RESULTS------------///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

public class results extends JFrame {
	

	private static final long serialVersionUID = 1L;

	
	private int posX = 0;   //Position X de la souris au clic
    private int posY = 0;   //Position Y de la souris au clic
    

	private JPanel contentPane;
	private JRadioButton RadiobtnYelp;
	private JRadioButton RadiobtnFilmTrust;
	private JRadioButton RadiobtnMovieLens1M;
	
	private int i=1; //deffiler les images
	private JScrollPane scrollpaneIMG; 

	

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
					results frame = new results("-1","NONE",false);
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
	public results(String dataset,String path_data,Boolean DataProcessed ) {
		setIconImage(Toolkit.getDefaultToolkit().getImage(results.class.getResource("/Menu_img/model.png")));
		//cnx

		setUndecorated(true);	
		setResizable(false);

		setTitle("Tests & Resulults");
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
		
		scrollpaneIMG = new JScrollPane();
		scrollpaneIMG.setBounds(412, 112,  640, 480);
		scrollpaneIMG.setBorder(BorderFactory.createEmptyBorder());
		scrollpaneIMG.getViewport().setOpaque(false);
		contentPane.add(scrollpaneIMG);
		
		
// le BG et lannimation////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		JLabel ModelsIMG = new JLabel("");
		scrollpaneIMG.setViewportView(ModelsIMG);
		
		JLabel BGModels = new JLabel("");
		BGModels.setIcon(new ImageIcon(results.class.getResource("/resulults_img/Tests & results.png")));
		//BGModels.setIcon(new ImageIcon(Models.class.getResource("/Menu_img/1.png")));	// Back ground de base	
       
// Bouton Reduire ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		JButton Minimise_BTN = new JButton("");
		Minimise_BTN.addMouseListener(new MouseAdapter() {
			@Override
			public void mouseEntered(MouseEvent e) {
				Minimise_BTN.setIcon(new ImageIcon(results.class.getResource("/Menu_img/Minimize ML selected.png")));
			}
			@Override
			public void mouseExited(MouseEvent e) {
				Minimise_BTN.setIcon(new ImageIcon(results.class.getResource("/Menu_img/Minimize ML .png")));
			}
		});
		Minimise_BTN.setToolTipText("Minimize");
		ButtonStyle(Minimise_BTN);
		Minimise_BTN.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				setState(ICONIFIED);
				
			}
		});
		Minimise_BTN.setIcon(new ImageIcon(results.class.getResource("/Menu_img/Minimize ML .png")));
		Minimise_BTN.setBounds(932, 11, 32, 32);
		contentPane.add(Minimise_BTN);
//Boutton home//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
				JButton btnHome = new JButton("");
				btnHome.addMouseListener(new MouseAdapter() {
					@Override
					public void mouseEntered(MouseEvent e) {
						if (btnHome.isEnabled()) {
							btnHome.setIcon(new ImageIcon(results.class.getResource("/Models_img/home selected.png")));//changer les couleurs button
						}
					}
					@Override
					public void mouseExited(MouseEvent e) {
						if (btnHome.isEnabled()) {
							btnHome.setIcon(new ImageIcon(results.class.getResource("/Models_img/home.png")));//remetre le bouton de base
						}
					}
				});
				btnHome.addActionListener(new ActionListener() {
					public void actionPerformed(ActionEvent e) {
							Menu frame = new Menu(dataset,path_data,DataProcessed);
							frame.setLocationRelativeTo(null);
							frame.setVisible(true);
							dispose();
					}
				});
				btnHome.setIcon(new ImageIcon(results.class.getResource("/Models_img/home.png")));
				btnHome.setToolTipText("Menu");
				btnHome.setBounds(974, 11, 32, 32);
				ButtonStyle(btnHome);
				contentPane.add(btnHome);
// Exit bouton//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		
		JButton Exit_BTN = new JButton("");
		Exit_BTN.addMouseListener(new MouseAdapter() {
			@Override
			public void mouseEntered(MouseEvent arg0) {
				Exit_BTN.setIcon(new ImageIcon(results.class.getResource("/Menu_img/Exit ML selected.png")));
			}
			@Override
			public void mouseExited(MouseEvent arg0) {
				Exit_BTN.setIcon(new ImageIcon(results.class.getResource("/Menu_img/Exit ML.png")));
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
		Exit_BTN.setIcon(new ImageIcon(results.class.getResource("/Menu_img/Exit ML.png")));
		Exit_BTN.setBounds(1016, 11, 32, 32);
		contentPane.add(Exit_BTN);
		
		
		
		JButton btnR = new JButton("");
		btnR.setIcon(new ImageIcon(results.class.getResource("/Models_img/next.png")));
		btnR.addMouseListener(new MouseAdapter() {
			@Override
			public void mouseEntered(MouseEvent arg0) {
				btnR.setIcon(new ImageIcon(results.class.getResource("/Models_img/next selected.png")));
			}
			@Override
			public void mouseExited(MouseEvent e) {
				btnR.setIcon(new ImageIcon(results.class.getResource("/Models_img/next.png")));
			}
		});
		btnR.setToolTipText("Next");
		btnR.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
			if(RadiobtnFilmTrust.isSelected()) {
				if (i==12)	i=0;
				if (i==13)	i=0;
				if (i<12) {
					i++;
					ModelsIMG.setIcon(new ImageIcon(results.class.getResource("/resulults_img/FT/"+i+".PNG")));
				}
			}
			if(RadiobtnMovieLens1M.isSelected()) {
				if (i==8)	i=0;
				if (i==9)	i=0;
				if (i<9) {
					i++;
					ModelsIMG.setIcon(new ImageIcon(results.class.getResource("/resulults_img/ML1M/"+i+".PNG")));
				}
			}
			if(RadiobtnYelp.isSelected()) {
				if (i==16)	i=0;
				if (i==17)	i=0;
				if (i<16) {
					i++;
					ModelsIMG.setIcon(new ImageIcon(results.class.getResource("/resulults_img/YELP/"+i+".PNG")));
				}
			}
				
			}
		});
		btnR.setBounds(1062, 314, 32, 32);
		ButtonStyle(btnR);
		contentPane.add(btnR);
		
		JButton btnL = new JButton("");
		btnL.setIcon(new ImageIcon(results.class.getResource("/Models_img/previous.png")));
		btnL.addMouseListener(new MouseAdapter() {
			@Override
			public void mouseEntered(MouseEvent e) {
				btnL.setIcon(new ImageIcon(results.class.getResource("/Models_img/previous selected.png")));
			}
			@Override
			public void mouseExited(MouseEvent e) {
				btnL.setIcon(new ImageIcon(results.class.getResource("/Models_img/previous.png")));
			}
		});
		btnL.setToolTipText("Previous");
		btnL.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				
				if(RadiobtnFilmTrust.isSelected()) {
					if (i==0)	i=12;
					if (i==1)	i=13;
					if (i>1) {
						i--;
						ModelsIMG.setIcon(new ImageIcon(results.class.getResource("/resulults_img/FT/"+i+".PNG")));
					}
					
				}
				if(RadiobtnMovieLens1M.isSelected()) {
					if (i==0)	i=8;
					if (i==1)	i=9;
					if (i>1) {
						i--;
						ModelsIMG.setIcon(new ImageIcon(results.class.getResource("/resulults_img/ML1M/"+i+".PNG")));
					}
					
				}
				if(RadiobtnYelp.isSelected()) {
					if (i==0)	i=16;
					if (i==1)	i=17;
					if (i>1) {
						i--;
						ModelsIMG.setIcon(new ImageIcon(results.class.getResource("/resulults_img/YELP/"+i+".PNG")));
					}
		
				}
				
			}
		});
		btnL.setBounds(374, 314, 32, 32);
		ButtonStyle(btnL);
		contentPane.add(btnL);
		
		RadiobtnYelp = new JRadioButton("");
		RadiobtnYelp.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				ModelsIMG.setIcon(new ImageIcon(results.class.getResource("/resulults_img/YELP/1.PNG")));
				i=1;
			}
		});
		RadiobtnYelp.setToolTipText("Yelp");
		RadiobtnYelp.setBounds(113, 215, 21, 23);
		contentPane.add(RadiobtnYelp);
		
		RadiobtnFilmTrust = new JRadioButton("");
		RadiobtnFilmTrust.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				ModelsIMG.setIcon(new ImageIcon(results.class.getResource("/resulults_img/FT/1.PNG")));
				i=1;
			}
		});
		RadiobtnFilmTrust.setToolTipText("Film Trust");
		RadiobtnFilmTrust.setBounds(113, 316, 21, 23);
		contentPane.add(RadiobtnFilmTrust);
		
		RadiobtnMovieLens1M = new JRadioButton("");
		RadiobtnMovieLens1M.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				ModelsIMG.setIcon(new ImageIcon(results.class.getResource("/resulults_img/ML1M/1.PNG")));
				i=1;
			}
		});
		RadiobtnMovieLens1M.setToolTipText("Movie Lens (1M)");
		RadiobtnMovieLens1M.setBounds(113, 413, 21, 23);
		contentPane.add(RadiobtnMovieLens1M);
		
		  //Group the radio buttons.
				ButtonGroup group = new ButtonGroup();
				group.add(RadiobtnYelp);
				group.add(RadiobtnFilmTrust);
				group.add(RadiobtnMovieLens1M);
		
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
