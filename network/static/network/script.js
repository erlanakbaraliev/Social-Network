// window.onpopstate = function(event) {
//     if (event.state) {
//         const state = event.state;
//         // Determine which view to load based on state.view
//         if (state.view === "allposts") {
//             loadView("#allpostsView");
//             displayPage(state.page || 1);
//         } else if (state.view === "profile") {
//             loadView("#profileView");
//             displayProfile(state.username, state.page || 1);
//         }
//     }
// };


document.addEventListener("DOMContentLoaded", ()=>{
    setupNavigation()
    loadView("#allpostsView")
    setupAllPostsPagination()
})

function setupNavigation() {
    const navigation = {
      '#allposts': () => {
        loadView('#allpostsView')
        
        // history.pushState({view: "allposts", page: 1}, "", "")
        displayPage(1)
    },
      '#profile': () => {
        loadView('#profileView')

        const profileButton = document.querySelector('#profile');
        const username = profileButton ? profileButton.dataset.username : null;
        if(username) {
            // history.pushState({ view: "profile", username: username, page: 1 }, "", `profile/${username}?page=1`);
            setupProfilePagination(username)
        }
    },
      '#following': () => {
        loadView("#followingView")
    },  
      '#followers': () => {
        loadView("#followersView")
      }
    };
  
    Object.entries(navigation).forEach(([selector, handlers]) => {
      const viewButton = document.querySelector(selector);
      if (viewButton) { 
        viewButton.addEventListener('click', (event) => {
          event.preventDefault();
          handlers()
        });
      }
    });
}

function loadView(viewId) {
    ['#allpostsView', '#profileView','#followingView', "#followersView"].forEach(id => {
        const div = document.querySelector(id)
        if(div) {
            div.style.display = id === viewId ? 'block' : 'none';
        }
      });
}

function setupAllPostsPagination() {
    const prevButton = document.querySelector("#all-prev");
    const nextButton = document.querySelector("#all-next");
    let pageNumber = 1;

    // Load initial page
    displayPage(pageNumber);

    // Handle Previous button click
    prevButton.addEventListener('click', (event) => {
        event.preventDefault();
        if (pageNumber > 1) {
            pageNumber--;
            displayPage(pageNumber);
        }
    });

    // Handle Next button click
    nextButton.addEventListener('click', (event) => {
        event.preventDefault();
        pageNumber++;
        displayPage(pageNumber);
    });
}

function displayPage(pageID) {
    fetch(`page/${pageID}`)
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.log(`PageID: ${pageID}`)
            console.error(data.error);
            return;
        }
        // Render the posts on the page
        renderPosts(data.posts, "#posts");

        // Get pagination buttons
        const prevButton = document.querySelector("#all-prev");
        const nextButton = document.querySelector("#all-next");

        // Enable/disable Previous button
        prevButton.disabled = !data.has_previous;
        nextButton.disabled = !data.has_next;
    })
    .catch(error => console.error("Error fetching page:", error));
}

function setupProfilePagination(username) {
    const prevButton = document.querySelector("#profile-prev");
    const nextButton = document.querySelector("#profile-next");
    let profilePageNumber = 1;
    
    displayProfile(username, profilePageNumber);

    prevButton.addEventListener('click', (event) => {
        event.preventDefault();
        if (profilePageNumber > 1) {
            profilePageNumber--;
            displayProfile(username, profilePageNumber);
        }
    });

    nextButton.addEventListener('click', (event) => {
        event.preventDefault();
        profilePageNumber++;
        displayProfile(username, profilePageNumber);
    });
}

function displayProfile(username, page=1) {
    fetch(`profile/${username}?page=${page}`)
    .then(response => response.json())
    .then(data => {
        // Render profile posts into the #profilePosts container
        renderPosts(data.posts, "#profilePosts");
        setupFollow(data.followed, data.followers)
        
        
        // Optionally, update the pagination buttons’ disabled state
        const prevButton = document.querySelector("#profile-prev");
        const nextButton = document.querySelector("#profile-next");
        prevButton.disabled = !data.has_previous;
        nextButton.disabled = !data.has_next;
    })
    .catch(error => console.error("Error fetching profile:", error));
}

function renderPosts(posts, divID) {
    const postsDiv = document.querySelector(`${divID}`);
    postsDiv.innerHTML = "";  // Clear current posts

    posts.forEach(post => {
        const postEl = document.createElement("div");
        postEl.className = "card";
        postEl.innerHTML = `
            <div class="card-body">
                <h4 class="card-title">@${post.user}</h4>
                <p class="card-text">${post.content.replace(/\n/g, '<br>')}</p>
                <p class="card-text"><small class="text-muted">${post.timedate}</small></p>
            </div>
        `;
        postsDiv.appendChild(postEl);
    });
}

function setupFollow(followed, followers) {
    renderFollow(followed.length, followers.length)

    // document.querySelector("#following").addEventListener('click', (event)=>{
        
    // })
    // document.querySelector("#followers").addEventListener('click', (event)=>{
    //     console.log("Followers clicked")
    // })
    
}

function renderFollow(followedCount, followersCount) {
    document.querySelector("#following").textContent = `Following: ${followedCount}`
    document.querySelector("#followers").textContent = `Followers: ${followersCount}`
}