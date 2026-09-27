(define (problem blocks-problem)
  (:domain BLOCKS)
  (:objects
    a - block
    b - block
    c - block
    d - block
    e - block
    f - block
    g - block
    h - block
  )
  (:init
    (handempty)
    (clear a)
    (on a g)
    (on g e)
    (ontable e)
    (clear d)
    (on d h)
    (on h f)
    (ontable f)
    (clear b)
    (ontable b)
    (clear c)
    (ontable c)
  )
  (:goal
    (and
      (on d f)
      (on f e)
      (on e h)
      (on h c)
      (on c a)
      (on a g)
      (on g b)
    )
  )
)
